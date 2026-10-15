import os
import sys
import urllib.request
import re
from html.parser import HTMLParser

class TableParser(HTMLParser):
    """Simple HTML parser to extract table cell contents."""
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = []
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.current_row = []
        elif tag in ['td', 'th']:
            self.in_cell = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            if self.current_row:
                self.rows.append(self.current_row)
        elif tag in ['td', 'th']:
            self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.current_row.append(data.strip())

def main():
    # 1. Check for CLI_VERSION environment variable
    cli_version = os.environ.get("CLI_VERSION")
    if not cli_version:
        print("Error: CLI_VERSION environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    # 2. Construct version repository URL
    base_url = f"https://sfc-repo.snowflakecomputing.com/snowflake-cli/windows_x86_64/{cli_version}/"
    index_url = f"{base_url}index.html"

    #print(f"Checking version {cli_version} at {index_url}...", file=sys.stderr)

    # 3. Attempt to fetch version directory index page
    try:
        req = urllib.request.Request(
            index_url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: Version '{cli_version}' does not exist in the repository (HTTP 404).", file=sys.stderr)
        else:
            print(f"Error: HTTP request failed with status code {e.code}.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to connect to repository: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Parse the HTML table to find the .msi file's SHA256 checksum
    parser = TableParser()
    parser.feed(html_content)

    checksum = None
    for row in parser.rows:
        row_text = " ".join(row)
        if ".msi" in row_text:
            for item in row:
                # Look for a standard 64-character hexadecimal SHA256 string
                if re.fullmatch(r"^[a-fA-F0-9]{64}$", item):
                    checksum = item
                    break
        if checksum:
            break

    # Fallback regex search if structural table parsing misses it
    if not checksum:
        hex_matches = re.findall(r'\b[a-fA-F0-9]{64}\b', html_content)
        if hex_matches:
            checksum = hex_matches[0]

    if not checksum:
        print(f"Error: Could not locate a valid SHA256 checksum for version '{cli_version}'.", file=sys.stderr)
        sys.exit(1)

    # Print log to stderr so it doesn't pollute the captured output
    #print(f"Success: Found SHA256 Checksum -> {checksum}", file=sys.stderr)

    # Print ONLY the raw checksum to stdout for PowerShell to capture
    print(checksum)

if __name__ == "__main__":
    main()
