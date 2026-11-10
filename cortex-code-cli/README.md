# Cortex Code CLI

This repository packages Snowflake Cortex Code CLI for Chocolatey. The steps below describe how to prepare, test, and publish a package manually.

## Build and test locally

Run PowerShell as Administrator. Move to the package directory and choose the Cortex Code CLI version to package.

```powershell
PS> cd <REPOSITORY_FOLDER>
PS> cd .\cortex-code-cli\
PS> $env:CLI_VERSION = "1.2.35"
PS> $env:CLI_VERSION
```

Look up the release metadata required by the installer: build number, commit hash, and SHA-256 checksum.

```powershell
PS> $env:VER_BUILD = (python tools/get_version.py -v $env:CLI_VERSION -r build)
PS> $env:VER_HASH = (python tools/get_version.py -v $env:CLI_VERSION -r hash)
PS> $env:SHA256_CHECKSUM = (python tools/get_version.py -v $env:CLI_VERSION -r checksum)
PS> $env:VER_BUILD
PS> $env:VER_HASH
PS> $env:SHA256_CHECKSUM
```

Create version-specific package and installer files. The substitutions fill in the selected version and release metadata.

```powershell
PS> (Get-Content cortex-code-cli.nuspec -Raw).Replace('x.y.z', $env:CLI_VERSION) | Set-Content cortex-code-cli.$env:CLI_VERSION.nuspec
PS> cd tools/
PS> (Get-Content chocolateyInstall.ps1 -Raw).Replace('$env:CLI_VERSION', $env:CLI_VERSION) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:VER_BUILD', $env:VER_BUILD) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:VER_HASH', $env:VER_HASH) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:SHA256_CHECKSUM', $env:SHA256_CHECKSUM) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> cd ..
```

Pack the Chocolatey package and install it from the local directory to verify it.

```powershell
PS> choco pack cortex-code-cli.$env:CLI_VERSION.nuspec
PS> choco uninstall cortex-code-cli --yes
PS> choco install cortex-code-cli --source . --yes --verbose
```

## Publish manually

Set your Chocolatey API key, then push the generated package to Chocolatey.

```powershell
PS> $env:YOUR_API_KEY = <YOUR_API_KEY>
PS> choco apikey --key $env:YOUR_API_KEY --source https://chocolatey.org
PS> choco push cortex-code-cli.$env:CLI_VERSION.nupkg --source https://chocolatey.org
```

Review package comments at https://community.chocolatey.org/packages/cortex-code-cli/<version>.

## Publish with GitHub Actions

Pushing a version tag triggers the GitHub Actions workflow for this package:

```bash
$ export version="1.2.35"
$ git tag v"$version"
$ git push origin v"$version"
```

## Install

Install a published version from Chocolatey:

```powershell
PS> choco install cortex-code-cli --version 1.2.35 --source https://chocolatey.org
```
