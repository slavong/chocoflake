# SnowCD

The Chocolatey package installs Snowflake's Windows 64-bit SnowCD connectivity diagnostic tool. SnowCD is end of life and no longer receives updates. Snowflake recommends using the `snow connection test` command in Snowflake CLI to test connectivity. See the [SnowCD documentation](https://docs.snowflake.com/en/user-guide/snowcd).

## Build and test locally

Run PowerShell as Administrator. From the repository root, move to this package directory and select a SnowCD version:

```powershell
PS> cd .\snowcd-cli\
PS> $env:SNOWCD_VERSION = "1.0.5"
```

The version helper can retrieve the latest available version and its MSI checksum:

```powershell
PS> $env:SNOWCD_VERSION = (python tools/get_version.py --return version)
PS> $env:SHA256_CHECKSUM = (python tools/get_version.py --version $env:SNOWCD_VERSION --return checksum)
```

Substitute the selected version and checksum in the package templates:

```powershell
PS> (Get-Content snowcd-cli.nuspec -Raw).Replace('x.y.z', $env:SNOWCD_VERSION) | Set-Content snowcd-cli.$env:SNOWCD_VERSION.nuspec
PS> (Get-Content tools\chocolateyInstall.ps1 -Raw).Replace('$env:SNOWCD_VERSION', $env:SNOWCD_VERSION).Replace('$env:SHA256_CHECKSUM', $env:SHA256_CHECKSUM) | Set-Content tools\chocolateyInstall.ps1
```

Pack the Chocolatey package and install it from the local directory to verify it:

```powershell
PS> choco pack snowcd-lci.$env:SNOWCD_VERSION.nuspec
PS> choco install snowcd-cli --source . --yes --verbose
```

## Publish with GitHub Actions

Pushing a tag in the form `vX.Y.Z-snowcd` publishes the package to Chocolatey and attaches the package files to the GitHub release.

```bash
$ export version="1.0.5"
$ git tag v"$version"-snowcd
$ git push origin v"$version"-snowcd
```

## Install

Install a published version from Chocolatey:

```powershell
PS> choco install snowcd --version 1.0.5 --source https://chocolatey.org
```
