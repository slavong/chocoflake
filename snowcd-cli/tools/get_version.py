import argparse
import hashlib
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List, Optional


BASE_URL = "https://sfc-repo.snowflakecomputing.com/snowcd/win64"
USER_AGENT = "Mozilla/5.0"
TIMEOUT = 30


class IndexParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: List[str] = []
        self.rows: List[List[Dict[str, Optional[str]]]] = []
        self.current_row: Optional[List[Dict[str, Optional[str]]]] = None
        self.current_cell: Optional[Dict[str, Optional[str]]] = None

    def handle_starttag(self, tag: str, attrs: list) -> None:
        tag = tag.lower()
        if tag == "tr":
            self.current_row = []
        elif tag in ("td", "th") and self.current_row is not None:
            self.current_cell = {"text": "", "href": None}
        elif tag == "a":
            href = next((value for key, value in attrs if key.lower() == "href"), None)
            if href:
                self.links.append(href)
                if self.current_cell is not None:
                    self.current_cell["href"] = href

    def handle_data(self, data: str) -> None:
        if self.current_cell is not None:
            self.current_cell["text"] = (self.current_cell["text"] or "") + data

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in ("td", "th") and self.current_cell is not None:
            self.current_cell["text"] = (self.current_cell["text"] or "").strip()
            if self.current_row is not None:
                self.current_row.append(self.current_cell)
            self.current_cell = None
        elif tag == "tr" and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP error {error.code} while retrieving {url}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Network error while retrieving {url}: {error.reason}") from error


def discover_versions() -> List[str]:
    parser = IndexParser()
    parser.feed(fetch_text(f"{BASE_URL}/index.html"))
    versions = {
        match.group(1)
        for link in parser.links
        if (match := re.fullmatch(r"(\d+(?:\.\d+)+)/index\.html", link))
    }
    if not versions:
        raise RuntimeError(f"No SnowCD versions found at {BASE_URL}/index.html")
    return sorted(versions, key=lambda version: tuple(map(int, version.split("."))))


def get_package_info(version: str) -> Dict[str, str]:
    index_url = f"{BASE_URL}/{urllib.parse.quote(version, safe='')}/index.html"
    parser = IndexParser()
    parser.feed(fetch_text(index_url))

    for row in parser.rows:
        msi = next(
            (cell for cell in row if cell["href"] and cell["href"].lower().endswith(".msi")),
            None,
        )
        if msi is None:
            continue

        download_url = urllib.parse.urljoin(index_url, msi["href"])
        file_name = urllib.parse.unquote(download_url.rsplit("/", 1)[-1])
        row_text = " ".join(cell["text"] or "" for cell in row)
        checksum = re.search(r"\b[a-fA-F0-9]{64}\b", row_text)
        if checksum:
            sha256 = checksum.group(0).lower()
        else:
            digest = hashlib.sha256()
            request = urllib.request.Request(download_url, headers={"User-Agent": USER_AGENT})
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                    while chunk := response.read(1024 * 1024):
                        digest.update(chunk)
            except urllib.error.URLError as error:
                raise RuntimeError(f"Unable to download {download_url}: {error}") from error
            sha256 = digest.hexdigest()

        return {
            "version": version,
            "checksum": sha256,
            "file_name": file_name,
            "download_url": download_url,
        }

    raise RuntimeError(f"No MSI found in SnowCD index: {index_url}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve SnowCD Windows MSI metadata.")
    parser.add_argument("--version", help="SnowCD version (defaults to the latest available)")
    parser.add_argument(
        "--return",
        dest="field",
        choices=("version", "checksum", "file_name", "download_url"),
        help="Print one metadata field",
    )
    args = parser.parse_args()

    try:
        versions = discover_versions()
        version = args.version or versions[-1]
        if version not in versions:
            raise RuntimeError(f"Version '{version}' not found in SnowCD index")
        info = get_package_info(version)
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    if args.field:
        print(info[args.field])
    else:
        for key, value in info.items():
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
