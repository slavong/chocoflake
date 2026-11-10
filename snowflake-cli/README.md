# Snowflake CLI

This repository packages Snowflake CLI for Chocolatey. The steps below describe how to prepare, test, and publish a package manually.

## Build and test locally

Run PowerShell as Administrator. First, move to the package directory and select the CLI version. Set a specific release:

```powershell
PS> cd <REPOSITORY_FOLDER>
PS> cd .\snowflake-cli\
PS> $env:CLI_VERSION = "3.29.0"
PS> $env:CLI_VERSION
```

Alternatively, retrieve the latest available release:

```powershell
PS> $env:CLI_VERSION = (python tools/get_latest_version.py)
PS> $env:CLI_VERSION
```

Look up the download's SHA-256 checksum. The package installer uses it to verify the downloaded CLI.

```powershell
PS> $env:SHA256_CHECKSUM = (python tools/check_snowflake_cli.py)
PS> $env:SHA256_CHECKSUM
```

Create version-specific package and installer files by substituting the selected version and checksum into the templates.

```powershell
PS> (Get-Content snowflake-cli.nuspec -Raw).Replace('x.y.z', $env:CLI_VERSION) | Set-Content snowflake-cli.$env:CLI_VERSION.nuspec
PS> cd tools/
PS> (Get-Content chocolateyInstall.ps1 -Raw).Replace('$env:CLI_VERSION', $env:CLI_VERSION) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:SHA256_CHECKSUM', $env:SHA256_CHECKSUM) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> cd ..
```

Pack the Chocolatey package and install it from the local directory to verify it.

```powershell
PS> choco pack snowflake-cli.$env:CLI_VERSION.nuspec
PS> choco uninstall snowflake-cli --yes
PS> choco install snowflake-cli --source . --yes --verbose
```

## Publish manually

Set your Chocolatey API key, then push the generated package to Chocolatey.

```powershell
PS> $env:YOUR_API_KEY = <YOUR_API_KEY>
PS> choco apikey --key $env:YOUR_API_KEY --source https://chocolatey.org
PS> choco push snowflake-cli.$env:CLI_VERSION.nupkg --source https://chocolatey.org
```

Review package comments at https://community.chocolatey.org/packages/snowflake-cli/<version>.

## Publish with GitHub Actions

Pushing a version tag triggers the GitHub Actions workflow for this package:

```bash
$ export version="3.29.0"
$ git tag v"$version"
$ git push origin v"$version"
```

## Install

Install a published version from Chocolatey:

```powershell
PS> choco install snowflake-cli --version 3.29.0 --source https://chocolatey.org
```
