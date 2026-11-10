$ErrorActionPreference = 'Stop'

Write-Host "Powershell version: $($PSVersionTable.PSVersion)"

$version = "$env:CLI_VERSION"
$checksum = "$env:SHA256_CHECKSUM" 

$dirName = "$version"
$fileName = "snowflake-odbc-$version.x86_64.msi"
$url = "https://sfc-repo.snowflakecomputing.com/odbc/win64/$dirName/$fileName"

Write-Host "Installing Snowflake ODBC driver version $version..."

Install-ChocolateyPackage `
  -PackageName 'snowflake-odbc-driver' `
  -FileType 'msi' `
  -SilentArgs '/qn /norestart' `
  -Url $url `
  -Checksum $checksum `
  -ChecksumType 'sha256'
