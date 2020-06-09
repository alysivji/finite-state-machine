import argparse
import os

import requests

GITHUB_OAUTH_TOKEN = os.getenv("GITHUB_OAUTH_TOKEN", None)
BASE_URL = "https://api.github.com"


def generate_changelog(owner, repo, version):
    github = GitHubClient()
    release_dt = github.get_release_date(owner, repo, version)
    messages = github.get_commit_messages(owner, repo, release_dt)

    # generate changelog
    if not messages:
        return []

    output = ["### Changes", ""]
    for message in messages:
        output.append("- " + message)
    return output


class GitHubClient:
    def __init__(self):
        headers = {
            "User-Agent": "Change Log",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        s = requests.session()
        s.headers.update(headers)
        self.session = s

    def get_release_date(self, owner, repo, version):
        url = f"{BASE_URL}/repos/{owner}/{repo}/releases/tags/{version}"
        resp = self.session.get(url)
        if resp.status_code == 404:
            raise ValueError("Version does not exist")
        resp.raise_for_status()

        return resp.json()["published_at"]

    def get_commit_messages(self, owner, repo, release_dt):
        url = f"{BASE_URL}/repos/{owner}/{repo}/commits"
        params = {"sha": "master", "since": release_dt}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()

        messages = [item.get("commit", {}).get("message") for item in resp.json()]
        return messages[::-1]


def parse_args():
    description = "Generate changelog for repository"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        help="Version to generate CHANGELOG from",
        required=True,
    )
    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    version = args["version"]
    owner = "alysivji"
    repo = "finite-state-machine"

    changelog = generate_changelog(owner, repo, version)
    print("\n".join(changelog))
