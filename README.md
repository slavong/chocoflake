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



```