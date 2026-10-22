import argparse
import re
import sys
from unittest import result

# The raw list provided previously
RAW_DATA = """
1.2.18+192728.aa2238062732 BDA2553F37E72E31FA4E44113BC3FC3EE733088C17C079535479C4E8316C7E65
1.2.14+213013.25aeae2a44ca
1.1.104+041358.66de1c44636f
1.1.87+175514.04f5c9114e11
1.1.84+190213.c06a9c29d351
1.1.78+212007.10798d3101f7
1.1.66+001753.801adc2b71d7
1.1.65+211353.f096733670be
1.1.60+201022.a3e8fc953384
1.1.58+010958.a47413fe34e5
1.1.53+181504.3a965a854064
1.1.52+200734.789ffffc1c9e
1.1.47+005207.7d03a05f5bd4
1.1.41+225157.0f36395f58d3
1.1.27+200623.07dcb388081e
1.1.24+222730.5ebfdc5bc920
1.1.15+215415.6cb780bd8e71
1.1.8+192013.01d33fc29c8e
1.1.6+214554.0e746c5289ad
1.1.5+221202.3129df38bece
1.1.2+165940.4c253edb86d7
1.1.1+001046.4c040d09e2a2
1.0.98+185601.3ff0835441f6
1.0.94+010053.1c830bb598fe
1.0.90+214902.b453c1a95f96
1.0.89+234231.508afd70db5c
1.0.88+195402.1229b547fbcf
1.0.87+182303.ed2703fb49ec
1.0.86+224640.05c0225c704f
1.0.85+235637.ba407a713a60
"""


def get_version_details(target_version):
  # Regex to match version+build.hash
  pattern = re.compile(
      r"^(?P<version>[^+]+)\+(?P<build>[^.]+)\.(?P<hash>[^/]+) (?P<checksum>[A-F0-9]+)"
  )

  for line in RAW_DATA.strip().splitlines():
    match = pattern.match(line.strip())
    if match:
      version = match.group("version")
      if version == target_version:
        return {
            "version": version,
            "build": match.group("build"),
            "hash": match.group("hash"),
            "checksum": match.group("checksum")
        }

  return None


def main():
  parser = argparse.ArgumentParser(
      description="Query build and hash for a specific version from text data."
  )
  parser.add_argument(
      "--version", required=True, help="The version to look up (e.g., 1.2.18)"
  )
  parser.add_argument(
      "--return",
      dest="return_val",
      choices=["version", "build", "hash", "checksum", "all"],
      default="all",
      help="What property to return (default: all)",
  )

  args = parser.parse_args()

  result = get_version_details(args.version)

  if not result:
    print(
        f"[ERROR] Version '{args.version}' was not found.",
        file=sys.stderr,
    )
    sys.exit(1)

  # Using dot notation for Namespace object (and dest='return_val' to avoid keyword collision)
  if args.return_val in ("version", "build", "hash", "checksum"):
    print(result[args.return_val])
  else:
    print(f"Version: {result['version']}")
    print(f"Build:   {result['build']}")
    print(f"Hash:    {result['hash']}")
    print(f"Checksum: {result['checksum']}")


if __name__ == "__main__":
  main()
