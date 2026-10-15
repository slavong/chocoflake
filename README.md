# chocoflake
chocolatey packages for snowflake tools

# Chocolatey
Using the latest available [chocolatey](https://chocolatey.org/) version 2.7.4 and Powershell version 7.6.6.

# How to build

Run Powershell as Administrator

```powershell
PS> cd <REPOSITORY_FOLDER>
PS> cd .\snowflake-cli\  

PS> choco pack snowflake-cli.nuspec

PS> choco uninstall snowflake-cli --yes
PS> choco install snowflake-cli --source . --yes --verbose

PS> choco apikey --key <YOUR_API_KEY> --source https://chocolatey.org
 
PS> choco push snowflake-cli.3.29.0.nupkg --source https://chocolatey.org
```

Review comments at https://community.chocolatey.org/packages/snowflake-cli/3.29.0

To trigger GitHub Actions script in this repository, tag the version
```bash
$ git tag v3.29.0
$ git push origin v3.29.0
```

Users can then install snowflake-cli using
```powershell
PS> choco install snowflake-cli --source https://chocolatey.org
```