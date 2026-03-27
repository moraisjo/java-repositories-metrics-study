import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
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
ITEMS_PER_PAGE = 10


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


def fetch_top_java_repositories(limit: int = DEFAULT_LIMIT, query_string: str = GITHUB_REPO_SEARCH_QUERY):
    """Fetch top Java repositories from GitHub using GraphQL API."""
    token = _get_github_token()
    
    # Load query from external file
    query_file = Path(__file__).parent / "github_query.graphql"
    query_template = _load_query(query_file)
    
    repositories = []
    cursor = None

    print(f"Fetching {limit} repositories...", file=sys.stderr)
    
    while len(repositories) < limit:
        remaining = limit - len(repositories)
        first = min(ITEMS_PER_PAGE, remaining)
        
        variables = {
            "first": first,
            "cursor": cursor,
            "queryString": query_string
        }
        
        payload = json.dumps({
            "query": query_template,
            "variables": variables
        }).encode("utf-8")
        
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

        try:
            with urllib.request.urlopen(request) as response:
                data = json.load(response)
        except urllib.error.HTTPError as exc:
            raise RuntimeError(exc.read().decode("utf-8", errors="replace")) from exc

        search = data["data"]["search"]
        repositories.extend(search["nodes"])
        
        print(f"Fetched {len(repositories)}/{limit} repositories...", file=sys.stderr)

        if not search["pageInfo"]["hasNextPage"]:
            break
        cursor = search["pageInfo"]["endCursor"]

    return repositories[:limit]


def export_to_csv(repositories: list, output_file: Path):
    """Export repositories to CSV file."""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'nameWithOwner',
            'url',
            'createdAt',
            'updatedAt',
            'stargazerCount',
            'forkCount',
            'watchersCount',
            'releasesCount',
            'mergedPullRequestsCount',
            'closedIssuesCount',
            'totalIssuesCount',
            'primaryLanguage'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for repo in repositories:
            # Flatten nested data structure
            row = {
                'nameWithOwner': repo.get('nameWithOwner', ''),
                'url': repo.get('url', ''),
                'createdAt': repo.get('createdAt', ''),
                'updatedAt': repo.get('updatedAt', ''),
                'age': (datetime.now(timezone.utc) - datetime.fromisoformat(repo.get('createdAt', '').replace('Z', '+00:00'))).days if repo.get('createdAt') else 0,
                'stargazerCount': repo.get('stargazerCount', 0),
                'forkCount': repo.get('forkCount', 0),
                'watchersCount': repo.get('watchers', {}).get('totalCount', 0),
                'releasesCount': repo.get('releases', {}).get('totalCount', 0),
                'mergedPullRequestsCount': repo.get('pullRequests', {}).get('totalCount', 0),
                'closedIssuesCount': repo.get('closedIssues', {}).get('totalCount', 0),
                'totalIssuesCount': repo.get('totalIssues', {}).get('totalCount', 0),
                'primaryLanguage': repo.get('primaryLanguage', {}).get('name', '') if repo.get('primaryLanguage') else ''
            }
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
    export_to_csv(repositories, output_file)


if __name__ == "__main__":
    main()
