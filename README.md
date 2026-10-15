# chocoflake
chocolatey packages for snowflake tools

# Chocolatey
Using the latest available [chocolatey](https://chocolatey.org/) version which is 7.6.6 as of time of writing.

# How to build

Run Powershell as Administrator

```ps1
PS> cd <repository folder>
PS> cd .\snowflake-cli\  

PS> choco pack snowflake-cli.nuspec

PS> choco uninstall snowflake-cli --yes
PS> choco install snowflake-cli --source . --yes --verbose

PS> choco apikey --key <YOUR_API_KEY> --source https://chocolatey.org
 
PS> choco push snowflake-cli.3.29.0.nupkg --source https://chocolatey.org
```

Review comments at https://community.chocolatey.org/packages/snowflake-cli/3.29.0

Users can install using
```ps1
PS> choco install snowflake-cli --source https://chocolatey.org
```