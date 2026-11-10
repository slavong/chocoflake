# Snowflake ODBC Driver

The Chocolatey package installs Snowflake's native Windows ODBC driver. A Snowflake account is required to use the driver. See the [Snowflake ODBC documentation](https://docs.snowflake.com/en/developer-guide/odbc/odbc) for driver details.

## Build and test locally

Run PowerShell as Administrator. From the repository root, move to the package directory and select the driver version. The version helper looks up the matching Windows 64-bit MSI in Snowflake's package repository.

```powershell
PS> cd .\snowflake-odbc-driver\
PS> $env:CLI_VERSION = "4.3.0"
PS> $env:CLI_VERSION
```

Retrieve the MSI's SHA-256 checksum. Chocolatey uses it to verify the downloaded installer.

```powershell
PS> $env:SHA256_CHECKSUM = (python tools/get_version.py --version $env:CLI_VERSION --return checksum)
PS> $env:SHA256_CHECKSUM
```

Substitute the selected version in the nuspec template and the version and checksum in the installer script.

```powershell
PS> (Get-Content snowflake-odbc-driver.nuspec -Raw).Replace('x.y.z', $env:CLI_VERSION) | Set-Content snowflake-odbc-driver.$env:CLI_VERSION.nuspec
PS> cd tools/
PS> (Get-Content chocolateyInstall.ps1 -Raw).Replace('$env:CLI_VERSION', $env:CLI_VERSION) | Set-Content chocolateyInstall.ps1
PS> (Get-Content chocolateyInstall.ps1 -Raw).Replace('$env:SHA256_CHECKSUM', $env:SHA256_CHECKSUM) | Set-Content chocolateyInstall.ps1
PS> cd ..
```

Pack the Chocolatey package and install it from the local directory to verify it.

```powershell
PS> choco pack snowflake-odbc-driver.$env:CLI_VERSION.nuspec
PS> choco install snowflake-odbc-driver --source . --yes --verbose
```

Replace `4.3.0` with the driver version you intend to package.

## Publish with GitHub Actions

Pushing a tag in the form `vX.Y.Z-odbc` triggers the workflow, which publishes the Chocolatey package and attaches the `.nuspec` and `.nupkg` files to the GitHub release.

```bash
$ export version="4.3.0"
$ git tag v"$version"-odbc
$ git push origin v"$version"-odbc
```

## Install

Install a published version from Chocolatey:

```powershell
PS> choco install snowflake-odbc-driver --version 4.3.0 --source https://chocolatey.org
```
