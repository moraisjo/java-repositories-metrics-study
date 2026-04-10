#!/usr/bin/env python3
"""
RQ03 pipeline: activity (number of releases) vs. quality (CK metrics).

This script reproduces the notebook flow in a regular Python script:
1. Load repository metadata from data/repositories.csv
2. Load and aggregate CK metrics (CBO, DIT, LCOM) per repository
3. Build and save analysis datasets/correlations
4. Generate scatter plots
5. Export report assets/markdown
"""

import argparse
import shutil
from pathlib import Path
from typing import Dict, Iterable, Optional

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr, spearmanr


# Use a non-interactive backend so the script runs in terminal/CI.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CK_METRICS = ["cbo", "dit", "lcom"]


def _resolve_path(project_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return project_root / path


def load_repositories(repo_csv: Path) -> pd.DataFrame:
    required_columns = {
        "nameWithOwner",
        "stargazerCount",
        "age",
        "releasesCount",
        "ckMetricsGenerated",
    }
    repos = pd.read_csv(
        repo_csv,
        parse_dates=["createdAt", "updatedAt"],
        dtype={"ckMetricsGenerated": "string"},
    )
    missing = required_columns.difference(repos.columns)
    if missing:
        cols = ", ".join(sorted(missing))
        raise ValueError(f"Missing required columns in {repo_csv}: {cols}")

    repos["ckMetricsGenerated"] = repos["ckMetricsGenerated"].str.lower()
    repos = repos[repos["ckMetricsGenerated"] == "true"].copy()
    repos["age_years"] = repos["age"] / 365.25
    if repos.empty:
        raise RuntimeError("No repositories with ckMetricsGenerated=true.")
    return repos


def load_ck_metrics(ck_dir: Path, repo_name_with_owner: str) -> Optional[pd.DataFrame]:
    safe_name = repo_name_with_owner.replace("/", "_")
    ck_path = ck_dir / safe_name / "ckMetrics.csv"
    if not ck_path.exists():
        return None

    df = pd.read_csv(ck_path)
    for metric in CK_METRICS:
        df[metric] = pd.to_numeric(df[metric], errors="coerce")
    return df


def summarize_ck(df: pd.DataFrame) -> Dict[str, float]:
    stats: Dict[str, float] = {"classes_n": float(len(df))}
    for metric in CK_METRICS:
        series = df[metric].dropna()
        stats[f"{metric}_mean"] = float(series.mean())
        stats[f"{metric}_median"] = float(series.median())
        stats[f"{metric}_std"] = float(series.std(ddof=1))
    return stats


def build_ck_summary(repos: pd.DataFrame, ck_dir: Path) -> pd.DataFrame:
    rows = []
    for name in repos["nameWithOwner"]:
        ck_df = load_ck_metrics(ck_dir, name)
        if ck_df is None:
            continue
        row = {"nameWithOwner": name}
        row.update(summarize_ck(ck_df))
        rows.append(row)

    summary = pd.DataFrame(rows)
    if summary.empty:
        raise RuntimeError("No CK summaries were generated. Check data/ck content.")
    return summary


def build_dataset(repos: pd.DataFrame, ck_summary: pd.DataFrame) -> pd.DataFrame:
    data = (
        repos.merge(ck_summary, on="nameWithOwner", how="inner")
        .assign(
            releases_count=lambda d: pd.to_numeric(d["releasesCount"], errors="coerce"),
            activity_releases=lambda d: np.log10(
                pd.to_numeric(d["releasesCount"], errors="coerce").clip(lower=0) + 1
            ),
        )
    )
    if data.empty:
        raise RuntimeError("Merged dataset is empty after joining repositories + CK summary.")
    return data


def correlation_row(df: pd.DataFrame, metric_col: str) -> Dict[str, float]:
    sub = df[["releases_count", metric_col]].dropna()
    if len(sub) < 2:
        return {
            "pearson": np.nan,
            "pearson_pvalue": np.nan,
            "spearman": np.nan,
            "spearman_pvalue": np.nan,
            "n": len(sub),
        }

    x = sub["releases_count"].to_numpy()
    y = sub[metric_col].to_numpy()
    pearson_coef, pearson_p = pearsonr(x, y)
    spearman_coef, spearman_p = spearmanr(x, y)

    return {
        "pearson": pearson_coef,
        "pearson_pvalue": pearson_p,
        "spearman": spearman_coef,
        "spearman_pvalue": spearman_p,
        "n": len(sub),
    }


def build_correlations(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metric in CK_METRICS:
        col = f"{metric}_median"
        row = {"metric": metric}
        row.update(correlation_row(data, col))
        rows.append(row)
    return pd.DataFrame(rows)


def save_scatter_plots(data: pd.DataFrame, fig_dir: Path) -> Iterable[Path]:
    fig_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for metric in CK_METRICS:
        y_col = f"{metric}_median"
        ax = sns.regplot(
            data=data,
            x="activity_releases",
            y=y_col,
            scatter_kws={"s": 12, "alpha": 0.35},
            line_kws={"color": "red"},
        )
        ax.set_title(f"Atividade (log10(releases + 1)) x {metric.upper()} (mediana)")
        ax.set_xlabel("log10(releases + 1)")
        ax.set_ylabel(metric.upper())

        fig = ax.get_figure()
        fig_path = fig_dir / f"rq03_{metric}_scatter.png"
        fig.savefig(fig_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        saved_paths.append(fig_path)

    return saved_paths


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    try:
        return df.to_markdown(index=False)
    except ImportError:
        # Fallback when tabulate is not installed.
        headers = list(df.columns)
        header = "| " + " | ".join(headers) + " |"
        sep = "| " + " | ".join(["---"] * len(headers)) + " |"
        rows = []
        for _, row in df.iterrows():
            values = [str(row[col]) for col in headers]
            rows.append("| " + " | ".join(values) + " |")
        return "\n".join([header, sep] + rows)


def export_report_assets(
    project_root: Path,
    figure_paths: Iterable[Path],
    corr_df: pd.DataFrame,
    corr_path: Path,
    ck_summary_path: Path,
    report_dir: Path,
) -> Path:
    assets_dir = report_dir / "assets" / "rq03"
    report_dir.mkdir(parents=True, exist_ok=True)
    assets_dir.mkdir(parents=True, exist_ok=True)

    copied_figs = []
    for src in sorted(figure_paths):
        dst = assets_dir / src.name
        shutil.copy2(src, dst)
        copied_figs.append(dst)

    corr_dst = assets_dir / "rq03_correlacoes.csv"
    if corr_path.exists():
        shutil.copy2(corr_path, corr_dst)

    ck_summary_dst = assets_dir / "rq03_resumo_por_repositorio.csv"
    if ck_summary_path.exists():
        shutil.copy2(ck_summary_path, ck_summary_dst)

    corr_table_md = dataframe_to_markdown(corr_df) if not corr_df.empty else "_Tabela vazia._"

    md_path = report_dir / "rq03_figuras.md"
    lines = [
        "# RQ03 - Graficos e Tabela de Correlacao",
        "",
        "## Correlacoes",
        "",
        corr_table_md,
        "",
        "## Graficos",
        "",
    ]
    for fig in copied_figs:
        rel = fig.relative_to(report_dir)
        title = fig.stem.replace("rq03_", "").replace("_scatter", "").upper()
        lines.extend([f"### {title}", f"![{title}]({rel.as_posix()})", ""])

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def parse_args() -> argparse.Namespace:
    script_root = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(
        description="Analyze activity vs CK quality metrics and export RQ03 artifacts."
    )
    parser.add_argument(
        "--project-root",
        default=str(script_root),
        help=f"Project root directory (default: {script_root})",
    )
    parser.add_argument(
        "--repositories-csv",
        default="data/repositories.csv",
        help="Repositories CSV path (relative to project root by default).",
    )
    parser.add_argument(
        "--ck-dir",
        default="data/ck",
        help="CK metrics base directory (relative to project root by default).",
    )
    parser.add_argument(
        "--summary-dir",
        default="data/summary",
        help="Directory to write summary CSVs.",
    )
    parser.add_argument(
        "--fig-dir",
        default="docs/figures",
        help="Directory to write figures.",
    )
    parser.add_argument(
        "--report-dir",
        default="docs/report",
        help="Directory to write report markdown/assets.",
    )
    parser.add_argument(
        "--skip-report",
        action="store_true",
        help="Skip report markdown/assets export.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    repo_csv = _resolve_path(project_root, args.repositories_csv)
    ck_dir = _resolve_path(project_root, args.ck_dir)
    summary_dir = _resolve_path(project_root, args.summary_dir)
    fig_dir = _resolve_path(project_root, args.fig_dir)
    report_dir = _resolve_path(project_root, args.report_dir)

    summary_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    pd.options.display.float_format = "{:.3f}".format
    sns.set_theme(style="whitegrid")

    repos = load_repositories(repo_csv)
    ck_summary = build_ck_summary(repos, ck_dir)
    ck_summary_path = summary_dir / "rq03_resumo_por_repositorio.csv"
    ck_summary.to_csv(ck_summary_path, index=False)
    data = build_dataset(repos, ck_summary)

    dataset_path = summary_dir / "rq03_dataset.csv"
    data.to_csv(dataset_path, index=False)

    corr_df = build_correlations(data)
    corr_path = summary_dir / "rq03_correlacoes.csv"
    corr_df.to_csv(corr_path, index=False)

    figure_paths = save_scatter_plots(data, fig_dir)

    print(f"Dataset saved: {dataset_path}")
    print(f"Correlations saved: {corr_path}")
    print(f"Figures saved: {fig_dir} ({len(list(figure_paths))} files)")

    if not args.skip_report:
        md_path = export_report_assets(
            project_root,
            figure_paths,
            corr_df,
            corr_path,
            ck_summary_path,
            report_dir,
        )
        print(f"Report markdown saved: {md_path}")


if __name__ == "__main__":
    main()
