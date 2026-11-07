# chocoflake
chocolatey packages for snowflake tools

# Chocolatey
Using the latest available [chocolatey](https://chocolatey.org/) version 2.7.4 and Powershell version 7.6.6.

# How to build Snowflake CLI

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

PS> cd tools/
PS> (Get-Content chocolateyInstall.ps1 -Raw).Replace('$env:CLI_VERSION', $env:CLI_VERSION) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:SHA256_CHECKSUM', $env:SHA256_CHECKSUM) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> cd ..

PS> choco pack snowflake-cli.$env:CLI_VERSION.nuspec

PS> choco uninstall snowflake-cli --yes
PS> choco install snowflake-cli --source . --yes --verbose

PS> $env:YOUR_API_KEY = <YOUR_API_KEY>
PS> choco apikey --key $env:YOUR_API_KEY --source https://chocolatey.org
 
PS> choco push snowflake-cli.$env:CLI_VERSION.nupkg --source https://chocolatey.org
```

Review comments at https://community.chocolatey.org/packages/snowflake-cli/<version>

To trigger GitHub Actions script in this repository, tag the version
```bash
$ export version="3.29.0"
$ git tag v"$version"
$ git push origin v"$version"
```

Users can then install snowflake-cli using
```powershell
PS> $env:CLI_VERSION = "3.29.0"
PS> choco install snowflake-cli --version $env:CLI_VERSION --source https://chocolatey.org
```


# How to build Cortex Code CLI

Run Powershell as Administrator

```powershell
PS> cd <REPOSITORY_FOLDER>
PS> cd .\cortex-code-cli\

PS> $env:CLI_VERSION = "1.2.35"
PS> $env:CLI_VERSION

PS> $env:VER_BUILD = (python tools/get_version.py -v $env:CLI_VERSION -r build)
PS> $env:VER_BUILD
PS> $env:VER_HASH = (python tools/get_version.py -v $env:CLI_VERSION -r hash)
PS> $env:VER_HASH
PS> $env:SHA256_CHECKSUM = (python tools/get_version.py -v $env:CLI_VERSION -r checksum)
PS> $env:SHA256_CHECKSUM

PS> (Get-Content cortex-code-cli.nuspec -Raw).Replace('x.y.z', $env:CLI_VERSION) | Set-Content cortex-code-cli.$env:CLI_VERSION.nuspec

PS> cd tools/
PS> (Get-Content chocolateyInstall.ps1 -Raw).Replace('$env:CLI_VERSION', $env:CLI_VERSION) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:VER_BUILD', $env:VER_BUILD) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:VER_HASH', $env:VER_HASH) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> (Get-Content chocolateyInstall.$env:CLI_VERSION.ps1 -Raw).Replace('$env:SHA256_CHECKSUM', $env:SHA256_CHECKSUM) | Set-Content chocolateyInstall.$env:CLI_VERSION.ps1
PS> cd ..

PS> choco pack cortex-code-cli.$env:CLI_VERSION.nuspec

PS> choco uninstall cortex-code-cli --yes
PS> choco install cortex-code-cli --source . --yes --verbose

PS> $env:YOUR_API_KEY = <YOUR_API_KEY>
PS> choco apikey --key $env:YOUR_API_KEY --source https://chocolatey.org
 
PS> choco push cortex-code-cli.$env:CLI_VERSION.nupkg --source https://chocolatey.org
```

Review comments at https://community.chocolatey.org/packages/cortex-code-cli/<version>

To trigger GitHub Actions script in this repository, tag the version
```bash
$ export version="1.2.35"
$ git tag v"$version"
$ git push origin v"$version"
```

Users can then install cortex-code-cli using
```powershell
PS> $env:CLI_VERSION = "1.2.35"
PS> choco install cortex-code-cli --version $env:CLI_VERSION --source https://chocolatey.org
```
