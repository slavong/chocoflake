
import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import hashlib

from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple

# Snowflake Cortex Code repository
BASE_URL = (
    "https://sfc-repo.snowflakecomputing.com/"
    "cortex-code-cli/windows_amd64"
)

USER_AGENT = "Mozilla/5.0"
TIMEOUT = 30



def calculate_sha256(url: str) -> str:
    """Download a file and calculate its SHA256 checksum."""

    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    sha256 = hashlib.sha256()

    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        while True:
            chunk = response.read(1024 * 1024)  # 1 MB
            if not chunk:
                break
            sha256.update(chunk)

    return sha256.hexdigest()


def fetch_url(url: str) -> str:
    """Fetch URL and return HTML/text content."""

    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read().decode("utf-8")


class DirectoryParser(HTMLParser):
    """Extract directory links from repository index."""

    def __init__(self):
        super().__init__()
        self.links: List[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            for key, value in attrs:
                if key.lower() == "href" and value:
                    self.links.append(value)


class IndexParser(HTMLParser):
    """Extract filename and checksum information from HTML tables."""

    def __init__(self):
        super().__init__()
        self.rows: List[List[Dict[str, Optional[str]]]] = []
        self.current_row = None
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()

        if tag == "tr":
            self.current_row = []

        elif tag in ("td", "th") and self.current_row is not None:
            self.current_cell = {
                "text": "",
                "href": None
            }

        elif tag == "a" and self.current_cell is not None:
            for key, value in attrs:
                if key.lower() == "href":
                    self.current_cell["href"] = value

    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_cell["text"] += data

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag in ("td", "th") and self.current_cell is not None:
            self.current_cell["text"] = (
                self.current_cell["text"].strip()
            )
            self.current_row.append(self.current_cell)
            self.current_cell = None

        elif tag == "tr" and self.current_row is not None:
            if self.current_row:
                self.rows.append(self.current_row)
            self.current_row = None


def parse_build_and_hash(
    full_version: str
) -> Tuple[Optional[str], Optional[str]]:
    """Extract build number and commit hash."""

    if "+" not in full_version:
        return None, None

    metadata = full_version.split("+", 1)[1]

    if "." in metadata:
        build, commit_hash = metadata.split(".", 1)
        return build, commit_hash

    return metadata, None


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read().decode("utf-8")

    
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import re


class DirectoryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            for key, value in attrs:
                if key.lower() == "href" and value:
                    self.links.append(value)


def resolve_full_version(short_version: str) -> str:

    if "+" in short_version:
        return short_version

    index_url = f"{BASE_URL}/index.html"
    html = fetch_text(index_url)

    parser = DirectoryParser()
    parser.feed(html)

    pattern = re.compile(
        rf"^{re.escape(short_version)}\+\d+\.[a-fA-F0-9]+/?$"
    )

    matches = []

    for href in parser.links:
        full_url = urljoin(index_url, href)
        path = unquote(urlsplit(full_url).path)

        parts = [part for part in path.split("/") if part]

        # Expected path:
        # cortex-code-cli/windows_amd64/<version>/index.html
        if len(parts) < 2 or parts[-1].lower() != "index.html":
            continue

        directory = parts[-2]

        if pattern.fullmatch(directory):
            matches.append(directory)

    if not matches:
        raise RuntimeError(
            f"Version '{short_version}' not found in {index_url}"
        )

    return max(
        set(matches),
        key=lambda v: int(re.search(r"\+(\d+)\.", v).group(1))
    )


def get_msi_info(full_version: str) -> Dict[str, str]:
    encoded_version = urllib.parse.quote(full_version, safe="")
    index_url = f"{BASE_URL}/{encoded_version}/index.html"

    html = fetch_url(index_url)

    parser = IndexParser()
    parser.feed(html)

    for row in parser.rows:
        msi_cell = None

        # Find the cell containing the MSI link
        for cell in row:
            href = cell.get("href")

            if not href:
                continue

            filename = urllib.parse.unquote(
                urllib.parse.urlsplit(href).path.rsplit("/", 1)[-1]
            )

            if filename.lower().endswith(".msi"):
                msi_cell = cell
                break

        if msi_cell is None:
            continue

        file_url = urllib.parse.urljoin(
            index_url, msi_cell["href"]
        )

        file_name = urllib.parse.unquote(
            urllib.parse.urlsplit(file_url).path.rsplit("/", 1)[-1]
        )

        # Check the entire row for a SHA256 value.
        row_text = " ".join(cell["text"] for cell in row)

        checksum_match = re.search(
            r"\b[a-fA-F0-9]{64}\b",
            row_text
        )

        if checksum_match:
            checksum = checksum_match.group(0).lower()
            print("SHA256 source: Snowflake repository index")
        else:
            print(
                f"SHA256 unavailable in index. "
                f"Downloading {file_name} to calculate it..."
            )
            checksum = calculate_sha256(file_url)
            print("SHA256 source: calculated from downloaded MSI")

        return {
            "file_name": file_name,
            "checksum": checksum,
            "index_url": index_url,
            "download_url": file_url,
        }

    raise RuntimeError(
        f"No MSI package found in repository index:\n{index_url}"
    )


def get_version_info(version: str) -> Dict[str, Optional[str]]:

    # Resolve version dynamically from repository index
    full_version = resolve_full_version(version)

    build_val, hash_val = parse_build_and_hash(full_version)

    # Retrieve MSI filename and SHA256
    package = get_msi_info(full_version)

    return {
        "version": full_version,
        "build": build_val,
        "hash": hash_val,
        "checksum": package["checksum"],
        "file_name": package["file_name"],
        "platform": "windows_amd64",
        "index_url": package["index_url"]
    }


def main():

    parser = argparse.ArgumentParser(
        description="Query Snowflake Cortex Code Windows AMD64 MSI metadata."
    )

    parser.add_argument(
        "-v",
        "--version",
        required=True,
        help="Version string, e.g. 1.2.35"
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
            "file_name"
        ],
        help="Return a single field as plain text."
    )

    args = parser.parse_args()

    data = get_version_info(args.version)

    if args.field:

        value = data.get(args.field)

        if value is not None:
            print(value)

    else:

        print(f"Full Version:       {data['version']}")
        print(f"Build:              {data['build']}")
        print(f"Hash:               {data['hash']}")
        print(f"MSI SHA256:         {data['checksum']}")
        print(f"File Name:          {data['file_name']}")
        print(f"Platform:           {data['platform']}")
        print(f"Index URL:          {data['index_url']}")


if __name__ == "__main__":
    main()
