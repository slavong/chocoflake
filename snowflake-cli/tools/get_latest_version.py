import os
import sys
import urllib.request
import re
from html.parser import HTMLParser

class TableParser(HTMLParser):
    """Extracts text data from table cells in the directory index HTML."""
    def __init__(self):
        super().__init__()
        self.versions = set()
        self.in_cell = False
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        if tag in ['td', 'th']:
            self.in_cell = True
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag in ['td', 'th']:
            self.in_cell = False
            # Clean up text (e.g., "3.29.0/" -> "3.29.0")
            cleaned = self.current_text.strip().rstrip('/')
            if re.match(r'^\d+(\.\d+)*$', cleaned):
                self.versions.add(cleaned)

    def handle_data(self, data):
        if self.in_cell:
            self.current_text += data

def parse_version(v_str):
    """Converts a version string into a tuple of integers for correct numerical sorting."""
    try:
        return tuple(map(int, v_str.split('.')))
    except ValueError:
        return (0,)

def main():
    url = "https://sfc-repo.snowflakecomputing.com/snowflake-cli/windows_x86_64/"
    
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error: Failed to connect to repository index: {e}", file=sys.stderr)
        sys.exit(1)

    # Parse table contents
    parser = TableParser()
    parser.feed(html_content)

    # Fallback to general regex search across the raw HTML if table parsing returns nothing
    if not parser.versions:
        found = re.findall(r'>\s*([\d\.]+(?:/\s*)?)<', html_content)
        for match in found:
            cleaned = match.strip().rstrip('/')
            if re.match(r'^\d+(\.\d+)*$', cleaned):
                parser.versions.add(cleaned)

    if not parser.versions:
        print("Error: No valid versions found in the repository index.", file=sys.stderr)
        sys.exit(1)

    # Find the maximum version logically (e.g., 3.29.0 > 3.10.1)
    max_version = max(parser.versions, key=parse_version)

    # Send logs to stderr so stdout remains clean
    #print(f"Latest available version: {max_version}", file=sys.stderr)

    # Print ONLY the version string to stdout
    print(max_version)

if __name__ == "__main__":
    main()
