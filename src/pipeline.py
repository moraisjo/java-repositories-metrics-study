import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
import re

GITHUB_API_URL = "https://api.github.com/graphql"
GITHUB_REPO_SEARCH_QUERY = "language:Java sort:stars"


def _get_github_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token

    bashrc = Path.home() / ".bashrc"
    if bashrc.exists():
        pattern = re.compile(r"^\s*(?:export\s+)?GITHUB_TOKEN\s*=\s*(.+?)\s*$")
        for line in bashrc.read_text(encoding="utf-8", errors="replace").splitlines():
            match = pattern.match(line)
            if not match:
                continue
            value = match.group(1).strip().strip('"').strip("'")
            if value:
                return value

    raise RuntimeError("GITHUB_TOKEN não encontradas.")


def fetch_top_java_repositories(limit: int = 1000):
    token = _get_github_token()
    repositories = []
    cursor = None

    while len(repositories) < limit:
        remaining = limit - len(repositories)
        first = 100 if remaining > 100 else remaining
        query = f"""
        query($first: Int!, $cursor: String) {{
          search(query: \"{GITHUB_REPO_SEARCH_QUERY}\", type: REPOSITORY, first: $first, after: $cursor) {{
            pageInfo {{
              hasNextPage
              endCursor
            }}
            nodes {{
              ... on Repository {{
                nameWithOwner
                url
                stargazerCount
              }}
            }}
          }}
        }}
        """
        payload = json.dumps({"query": query, "variables": {"first": first, "cursor": cursor}}).encode("utf-8")
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

        if not search["pageInfo"]["hasNextPage"]:
            break
        cursor = search["pageInfo"]["endCursor"]

    return repositories[:limit]


def main():
    repositories = fetch_top_java_repositories()
    json.dump(repositories, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
