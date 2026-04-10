import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Tuple
import urllib.error
import urllib.request

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file
except ImportError:
    pass  # dotenv is optional

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_REPO_SEARCH_QUERY = "language:Java sort:stars"
DEFAULT_OUTPUT_FILE = "data/repositories.csv"
DEFAULT_LIMIT = 1000
ITEMS_PER_PAGE = 20
HTTP_MAX_RETRIES = 5
HTTP_TIMEOUT_SECONDS = 60
BASE_FIELDS = [
    "nameWithOwner",
    "url",
    "createdAt",
    "updatedAt",
    "age",
    "stargazerCount",
    "forkCount",
    "watchersCount",
    "releasesCount",
    "mergedPullRequestsCount",
    "closedIssuesCount",
    "totalIssuesCount",
    "primaryLanguage",
]


def _get_github_token() -> str:
    """Get GitHub token from environment variable."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "GITHUB_TOKEN não encontrado. "
            "Configure a variável de ambiente ou use um arquivo .env"
        )
    return token


def _load_query(query_file: Path) -> str:
    """Load GraphQL query from external file."""
    if not query_file.exists():
        raise FileNotFoundError(f"Query file not found: {query_file}")
    return query_file.read_text(encoding="utf-8")


def _run_graphql_query(token: str, query_template: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    payload = json.dumps({"query": query_template, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        GITHUB_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github+json",
        },
        method="POST",
    )

    data = None
    for attempt in range(1, HTTP_MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
                data = json.load(response)
            break
        except urllib.error.HTTPError as exc:
            should_retry = exc.code >= 500 and attempt < HTTP_MAX_RETRIES
            if should_retry:
                wait_s = min(2 ** (attempt - 1), 8)
                print(
                    f"Transient GitHub API error {exc.code}, retrying in {wait_s}s "
                    f"(attempt {attempt}/{HTTP_MAX_RETRIES})...",
                    file=sys.stderr,
                )
                time.sleep(wait_s)
                continue
            raise RuntimeError(exc.read().decode("utf-8", errors="replace")) from exc
        except urllib.error.URLError as exc:
            if attempt < HTTP_MAX_RETRIES:
                wait_s = min(2 ** (attempt - 1), 8)
                print(
                    f"Network error ({exc.reason}), retrying in {wait_s}s "
                    f"(attempt {attempt}/{HTTP_MAX_RETRIES})...",
                    file=sys.stderr,
                )
                time.sleep(wait_s)
                continue
            raise RuntimeError(f"Network error during GitHub query: {exc.reason}") from exc

    if data is None:
        raise RuntimeError("Failed to fetch data from GitHub API after retries.")
    return data


def _fetch_query_chunk(
    token: str,
    query_template: str,
    query_string: str,
    chunk_limit: int,
) -> List[Dict[str, Any]]:
    repositories: List[Dict[str, Any]] = []
    cursor = None

    while len(repositories) < chunk_limit:
        remaining = chunk_limit - len(repositories)
        first = min(ITEMS_PER_PAGE, remaining)
        variables = {"first": first, "cursor": cursor, "queryString": query_string}
        data = _run_graphql_query(token, query_template, variables)
        search = data["data"]["search"]
        repositories.extend(search["nodes"])
        if len(repositories) % 100 == 0 or len(repositories) >= chunk_limit:
            print(
                f"  chunk '{query_string}' progress: {len(repositories)}/{chunk_limit}",
                file=sys.stderr,
            )

        if not search["pageInfo"]["hasNextPage"]:
            break
        cursor = search["pageInfo"]["endCursor"]

    return repositories[:chunk_limit]


def fetch_top_java_repositories(limit: int = DEFAULT_LIMIT, query_string: str = GITHUB_REPO_SEARCH_QUERY):
    """Fetch top Java repositories from GitHub using GraphQL API."""
    token = _get_github_token()
    
    # Load query from external file
    query_file = Path(__file__).parent / "github_query.graphql"
    query_template = _load_query(query_file)

    print(f"Fetching {limit} repositories...", file=sys.stderr)

    repositories: List[Dict[str, Any]] = []
    seen_repos = set()
    stars_ceiling: int | None = None

    while len(repositories) < limit:
        remaining = limit - len(repositories)
        chunk_limit = min(remaining, 1000)
        current_query = query_string
        if stars_ceiling is not None:
            current_query = f"language:Java stars:<={stars_ceiling} sort:stars"

        chunk = _fetch_query_chunk(token, query_template, current_query, chunk_limit)
        if not chunk:
            break

        added = 0
        for repo in chunk:
            name = repo.get("nameWithOwner")
            if not name or name in seen_repos:
                continue
            repositories.append(repo)
            seen_repos.add(name)
            added += 1
            if len(repositories) >= limit:
                break

        print(f"Fetched {len(repositories)}/{limit} repositories...", file=sys.stderr)

        if len(repositories) >= limit:
            break
        if added == 0:
            break

        star_values = [
            int(repo.get("stargazerCount", 0))
            for repo in chunk
            if repo.get("stargazerCount") is not None
        ]
        if not star_values:
            break

        next_ceiling = min(star_values) - 1
        if next_ceiling < 0:
            break
        if stars_ceiling is not None and next_ceiling >= stars_ceiling:
            break
        stars_ceiling = next_ceiling

    return repositories[:limit]


def _load_existing_metadata(output_file: Path) -> Tuple[Dict[str, Dict[str, str]], List[str]]:
    """
    Load extra columns from an existing CSV so they can be preserved on refresh.

    Returns:
        Tuple(existing_by_repo, extra_fieldnames)
    """
    if not output_file.exists():
        return {}, []

    with open(output_file, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        if not reader.fieldnames or "nameWithOwner" not in reader.fieldnames:
            return {}, []

        extra_fields = [f for f in reader.fieldnames if f not in BASE_FIELDS]
        existing: Dict[str, Dict[str, str]] = {}
        for row in reader:
            name = row.get("nameWithOwner", "")
            if not name:
                continue
            existing[name] = {f: row.get(f, "") for f in extra_fields}
        return existing, extra_fields


def export_to_csv(
    repositories: list,
    output_file: Path,
    existing_by_repo: Dict[str, Dict[str, str]] | None = None,
    extra_fields: List[str] | None = None,
):
    """Export repositories to CSV file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    existing_by_repo = existing_by_repo or {}
    extra_fields = extra_fields or []
    
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [*BASE_FIELDS, *extra_fields]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for repo in repositories:
            # Flatten nested data structure
            row = {
                "nameWithOwner": repo.get("nameWithOwner", ""),
                "url": repo.get("url", ""),
                "createdAt": repo.get("createdAt", ""),
                "updatedAt": repo.get("updatedAt", ""),
                "age": (
                    datetime.now(timezone.utc)
                    - datetime.fromisoformat(repo.get("createdAt", "").replace("Z", "+00:00"))
                ).days
                if repo.get("createdAt")
                else 0,
                "stargazerCount": repo.get("stargazerCount", 0),
                "forkCount": repo.get("forkCount", 0),
                "watchersCount": repo.get("watchers", {}).get("totalCount", 0),
                "releasesCount": repo.get("releases", {}).get("totalCount", 0),
                "mergedPullRequestsCount": repo.get("pullRequests", {}).get("totalCount", 0),
                "closedIssuesCount": repo.get("closedIssues", {}).get("totalCount", 0),
                "totalIssuesCount": repo.get("totalIssues", {}).get("totalCount", 0),
                "primaryLanguage": repo.get("primaryLanguage", {}).get("name", "") if repo.get("primaryLanguage") else "",
            }

            previous = existing_by_repo.get(row["nameWithOwner"], {})
            for field in extra_fields:
                row[field] = previous.get(field, "")

            writer.writerow(row)
    
    print(f"Exported {len(repositories)} repositories to {output_file}", file=sys.stderr)


def count_csv_rows(csv_file: Path) -> int:
    """Count the number of rows (excluding header) in a CSV file."""
    if not csv_file.exists():
        return 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        return sum(1 for _ in csv.reader(f)) - 1  # Subtract header row


def main():
    parser = argparse.ArgumentParser(
        description="Fetch top Java repositories from GitHub and export to CSV"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help=f"Number of repositories to fetch (default: {DEFAULT_LIMIT})"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output CSV file path (default: {DEFAULT_OUTPUT_FILE})"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-fetch even if output file already has enough repositories"
    )
    
    args = parser.parse_args()
    output_file = Path(args.output)
    existing_by_repo, extra_fields = _load_existing_metadata(output_file)
    
    # Check if CSV already exists with enough data
    if not args.force:
        existing_count = count_csv_rows(output_file)
        if existing_count >= args.limit:
            print(
                f"CSV file already exists with {existing_count} repositories "
                f"(>= {args.limit} requested). Skipping fetch.",
                file=sys.stderr
            )
            print(f"Use --force to re-fetch anyway.", file=sys.stderr)
            return
        elif existing_count > 0:
            print(
                f"CSV file exists with only {existing_count} repositories "
                f"(< {args.limit} requested). Fetching data...",
                file=sys.stderr
            )
    
    # Fetch repositories
    repositories = fetch_top_java_repositories(limit=args.limit)
    
    # Export to CSV
    export_to_csv(repositories, output_file, existing_by_repo=existing_by_repo, extra_fields=extra_fields)


if __name__ == "__main__":
    main()
