# Architectural & Implementation Decisions

This document records the key decisions made throughout the project, in chronological order.

---

## D01 — GraphQL over REST for GitHub data collection
**Decision:** Use the GitHub GraphQL API instead of the REST API.  
**Rationale:** A single GraphQL request can fetch all required fields (stars, forks, watchers, releases, pull requests, issues, language) in one round trip. The REST API would require separate calls to multiple endpoints per repository, multiplying latency and rate-limit consumption across 1 000 repos.

---

## D02 — External `.graphql` file for the query
**Decision:** Store the GraphQL query in `src/github_query.graphql` rather than embedding it as a Python string.  
**Rationale:** Keeps the query readable, diffable, and editable without touching Python code. GraphQL syntax highlighting also works in editors.

---

## D03 — CSV as the primary data interchange format
**Decision:** Export GitHub repository data to `data/repositories.csv`.  
**Rationale:** CSV is universally readable (pandas, Excel, R, LibreOffice) and portable. For a research dataset of 1 000 rows with flat fields, the overhead of a relational database is not justified.

---

## D04 — `age` field computed at collection time
**Decision:** Add an `age` column to the CSV, calculated as `(now − createdAt).days` during export.  
**Rationale:** RQ02 (Maturity) needs a numeric age value. Computing it once at collection time ensures all analyses share the same baseline date and avoids repeated datetime arithmetic downstream.

---

## D05 — CK tool pinned as a Git submodule
**Decision:** Add `source-code-ck/ck` as a Git submodule pointing to a specific CK commit.  
**Rationale:** Pins the exact version of the analysis tool, making the study fully reproducible. Anyone cloning the repo with `--recurse-submodules` gets the identical JAR.

---

## D06 — Shallow clone (`--depth 1`) for analysed repositories
**Decision:** Clone repositories with `--depth 1` before CK analysis.  
**Rationale:** CK only needs source files, not commit history. A shallow clone is orders of magnitude faster and uses far less disk space, which matters when processing hundreds of repositories.

---

## D07 — SSH as default clone protocol (HTTPS optional)
**Decision:** Default to `git@github.com:owner/repo.git` with an opt-in `--use-http` flag.  
**Rationale:** SSH avoids GitHub token exposure in process lists and is typically pre-configured on developer machines. HTTPS is provided as a fallback for environments without SSH keys.

---

## D08 — Idempotent runs via `ckMetricsGenerated` flag
**Decision:** Track analysis status per repository with a `ckMetricsGenerated` column (`true` / `false` / empty) in the CSV.  
**Rationale:** Analysis of 1 000 repos can take many hours and may be interrupted. The flag lets the pipeline resume from where it left off without reprocessing already-completed repositories. `--force` overrides this.

---

## D09 — Parallel analysis with `ThreadPoolExecutor`
**Decision:** Run CK analysis concurrently using Python's `ThreadPoolExecutor`.  
**Rationale:** Clone + CK analysis per repo is dominated by I/O and JVM startup. True parallelism (via threads that spawn subprocesses) allows multiple repos to be processed simultaneously, cutting total wall-clock time significantly.

---

## D10 — Default parallelism raised from 3 → 10, then lowered back to 3
**Decision:** Default `--parallel` is now 3.  
**Rationale:** Running 10 JVM instances simultaneously caused OS-level OOM kills (`SIGKILL`) on machines with ≤ 16 GB RAM: each CK instance for a large repo can consume 2–4 GB. Three parallel jobs is a safe default while still providing a 3× speedup; users with more RAM can override via `--parallel`.

---

## D11 — JVM heap limit per CK instance (`-Xmx2g`)
**Decision:** Pass `-Xmx{jvm_memory}` (default `2g`) and `-Xms512m` to every `java -jar ck.jar` invocation. Exposed as `--jvm-memory`.  
**Rationale:** Without a heap cap the JVM can grow unboundedly, causing SIGKILL when multiple parallel instances compete for memory. An explicit ceiling makes memory consumption predictable. Users with large RAM and only a few repos can raise it (e.g. `--jvm-memory 8g`).

---

## D12 — CK `max-files-per-partition` set to 500 (was 0 = unlimited)
**Decision:** Pass `500` as the `max-files-per-partition` argument to CK instead of `0`. Exposed as `--max-files`.  
**Rationale:** With `0` CK loads all Java files into a single partition. For very large repositories (Elasticsearch, Apache Kafka, Spring Framework, Apache Flink) this exhausts the heap and either triggers OOM or causes analysis to time out. Partitioning into batches of 500 files keeps per-partition memory bounded and allows CK to finish within the 20-minute timeout.

---

## D13 — Stderr captured and logged on CK failure
**Decision:** On `CalledProcessError`, print the first 30 lines of CK's stderr to help diagnose `exit status 1` failures.  
**Rationale:** Previously all non-zero exits from CK produced the same opaque message. Surfacing stderr makes it possible to distinguish parse errors, unsupported Java versions, JVM crashes, and other CK-specific failures.

---

## D14 — `--skip-failed` flag to exclude previously-failed repos
**Decision:** Add `--skip-failed` flag. When set, repos with `ckMetricsGenerated=false` are excluded from the pending queue. Default: retry all non-successful.  
**Rationale:** After applying fixes (D11, D12) users want to retry failed repos, so by default they stay in the queue. `--skip-failed` is useful for runs where the user knows certain repos are permanently unprocessable (e.g. repos that consistently exceed any reasonable timeout).

---

## D15 — Clone timeout extended from 600 s → 900 s
**Decision:** Increase `git clone` timeout from 10 min to 15 min.  
**Rationale:** `openjdk/jdk` and similar monorepo-scale repositories timed out at 600 s even with `--depth 1`. 900 s provides headroom for slow network conditions without blocking the pipeline indefinitely.
