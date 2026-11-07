
import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

# Snowflake Cortex Code repository
S3_BUCKET = "sfc-repo.snowflakecomputing.com"
S3_PREFIX = "cortex-code-cli/a4643c4278"
BASE_URL = f"https://{S3_BUCKET}/{S3_PREFIX}"

USER_AGENT = "Mozilla/5.0"
TIMEOUT = 20


class LinkParser(HTMLParser):
    """Extract links from an HTML directory listing."""

    def __init__(self):
        super().__init__()
        self.links: List[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            for key, value in attrs:
                if key.lower() == "href" and value:
                    self.links.append(value)


def fetch_url(url: str) -> str:
    """Fetch URL and return its content as text."""

    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read().decode("utf-8")


def get_platform_dir(os_name: str, arch: str) -> str:
    """Map OS and architecture to Snowflake package naming."""

    mapping = {
        ("windows", "amd64"): "windows-amd64",
        ("linux", "amd64"): "linux-amd64",
        ("linux", "arm64"): "linux-arm64",
        ("darwin", "arm64"): "darwin-arm64",
        ("darwin", "amd64"): "darwin-amd64",
    }

    return mapping.get(
        (os_name.lower(), arch.lower()),
        f"{os_name.lower()}-{arch.lower()}"
    )


def parse_build_and_hash(
    full_version: str
) -> Tuple[Optional[str], Optional[str]]:
    """Extract build number and commit hash from full version."""

    if "+" not in full_version:
        return None, None

    metadata = full_version.split("+", 1)[1]

    if "." in metadata:
        build, commit_hash = metadata.split(".", 1)
        return build, commit_hash

    return metadata, None


def resolve_full_version(short_version: str) -> str:
    """
    Resolve a short version (e.g. 1.2.35) to its full version
    (e.g. 1.2.35+123456.abcdef).

    Resolution order:
      1. Direct full version supplied by user
      2. Stable, beta and dev channel pointers
      3. Repository directory listing (historical versions)
    """

    if "+" in short_version:
        return short_version

    # 1. Check channel pointers
    for channel in ("stable", "beta", "dev"):

        channel_url = f"{BASE_URL}/{channel}_version.txt"

        try:
            candidate = fetch_url(channel_url).strip()

            if (
                candidate == short_version
                or candidate.startswith(short_version + "+")
            ):
                return candidate

        except (urllib.error.URLError, TimeoutError):
            continue

    # 2. Search repository directory listing
    try:
        html_data = fetch_url(BASE_URL + "/")

        parser = LinkParser()
        parser.feed(html_data)

        matches = set()

        for link in parser.links:

            # Extract directory name
            name = urllib.parse.unquote(link.rstrip("/").split("/")[-1])

            # Match exact short version followed by build metadata
            if name.startswith(short_version + "+"):

                if re.fullmatch(
                    re.escape(short_version)
                    + r"\+[a-zA-Z0-9_.-]+",
                    name
                ):
                    matches.add(name)

        if matches:
            # Return latest lexicographically sorted candidate
            return sorted(matches, reverse=True)[0]

    except urllib.error.HTTPError as e:
        sys.exit(
            f"HTTP error {e.code} querying repository directory listing."
        )

    except urllib.error.URLError as e:
        sys.exit(
            f"Network error querying repository: {e.reason}"
        )

    sys.exit(
        f"Error: Could not resolve full version '{short_version}'. "
        "No matching channel pointer or version directory was found."
    )


def get_version_info(
    version: str,
    os_name: str = "windows",
    arch: str = "amd64"
) -> Dict[str, Any]:

    # Resolve full version
    full_version = resolve_full_version(version)

    build_val, hash_val = parse_build_and_hash(full_version)

    platform_dir = get_platform_dir(os_name, arch)

    # Encode '+' as '%2B' in the URL
    encoded_version = urllib.parse.quote(full_version, safe="")

    # Manifest is located directly under the version directory
    manifest_url = (
        f"{BASE_URL}/{encoded_version}/manifest.json"
    )

    try:
        manifest_data = json.loads(fetch_url(manifest_url))

    except urllib.error.HTTPError as e:
        sys.exit(
            f"HTTP error {e.code} fetching manifest:\n{manifest_url}"
        )

    except urllib.error.URLError as e:
        sys.exit(
            f"Network error accessing manifest: {e.reason}"
        )

    except json.JSONDecodeError as e:
        sys.exit(f"Invalid manifest JSON: {e}")

    # Extract package metadata
    packages = manifest_data.get("packages", {})

    target_package = (
        packages.get(os_name, {}).get(arch)
    )

    if not target_package:
        sys.exit(
            f"No package found for {os_name}/{arch} "
            f"in version '{full_version}'."
        )

    return {
        "version": full_version,
        "build": build_val,
        "hash": hash_val,
        "checksum (sha256)": target_package.get("checksum"),
        "file_name": target_package.get("name"),
        "platform": platform_dir,
        "manifest_url": manifest_url,
    }


def main():

    parser = argparse.ArgumentParser(
        description="Query Snowflake Cortex CLI version metadata."
    )

    parser.add_argument(
        "-v",
        "--version",
        required=True,
        help="Version string (e.g. 1.2.35 or full version)"
    )

    parser.add_argument(
        "-r",
        "--return",
        dest="field",
        choices=[
            "build",
            "hash",
            "checksum",
            "version",
            "file_name",
        ],
        help="Return a single field as plain text."
    )

    parser.add_argument(
        "--os",
        default="windows",
        choices=["windows", "linux", "darwin"],
        help="Target operating system (default: windows)"
    )

    parser.add_argument(
        "--arch",
        default="amd64",
        choices=["amd64", "arm64"],
        help="Target architecture (default: amd64)"
    )

    args = parser.parse_args()

    data = get_version_info(
        args.version,
        os_name=args.os,
        arch=args.arch
    )

    field_mapping = {
        "build": data["build"],
        "hash": data["hash"],
        "checksum": data["checksum (sha256)"],
        "version": data["version"],
        "file_name": data["file_name"],
    }

    if args.field:

        value = field_mapping[args.field]

        if value is not None:
            print(value)

    else:

        print(f"Full Version:       {data['version']}")
        print(f"Build:              {data['build']}")
        print(f"Hash:               {data['hash']}")
        print(f"Checksum (sha256):  {data['checksum (sha256)']}")
        print(f"File Name:          {data['file_name']}")
        print(f"Platform:           {data['platform']}")
        print(f"Manifest URL:       {data['manifest_url']}")


if __name__ == "__main__":
    main()
