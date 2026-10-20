# chocoflake
chocolatey packages for snowflake tools

# Chocolatey
Using the latest available [chocolatey](https://chocolatey.org/) version 2.7.4 and Powershell version 7.6.6.

# How to build

Run Powershell as Administrator

```powershell
PS> cd <REPOSITORY_FOLDER>
PS> cd .\snowflake-cli\  

PS> $env:CLI_VERSION = "3.29.0"
PS> $env:CLI_VERSION = (python tools/get_latest_version.py)
PS> $env:CLI_VERSION

PS> $env:SHA256_CHECKSUM = (python tools/check_snowflake_cli.py)
PS> $env:SHA256_CHECKSUM

PS> (Get-Content snowflake-cli.nuspec -Raw).Replace('x.y.z', $env:CLI_VERSION) | Set-Content snowflake-cli.$env:CLI_VERSION.nuspec
PS> choco pack snowflake-cli.$env:CLI_VERSION.nuspec

PS> cd tools/
PS> (Get-Content chocolateyInstall.ps1 -Raw).Replace('$env:CLI_VERSION', $env:CLI_VERSION) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:SHA256_CHECKSUM', $env:SHA256_CHECKSUM) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> cd ..

PS> choco uninstall snowflake-cli --yes
PS> choco install snowflake-cli --source . --yes --verbose

PS> $env:YOUR_API_KEY = <YOUR_API_KEY>
PS> choco apikey --key $env:YOUR_API_KEY --source https://chocolatey.org
 
PS> choco push snowflake-cli.$env:CLI_VERSION.nupkg --source https://chocolatey.org
```

Review comments at https://community.chocolatey.org/packages/snowflake-cli/<version>

To trigger GitHub Actions script in this repository, tag the version
```bash
$ export version="3.2.9"
$ git tag v"$version"
$ git push origin v"$version"
```

Users can then install snowflake-cli using
```powershell
PS> $env:CLI_VERSION = "3.29.0"
PS> choco install snowflake-cli --version $env:CLI_VERSION --source https://chocolatey.org
```