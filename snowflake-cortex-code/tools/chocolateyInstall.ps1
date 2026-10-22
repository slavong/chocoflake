$ErrorActionPreference = 'Stop'

Write-Host "Powershell version: $($PSVersionTable.PSVersion)"

$version = "$env:CLI_VERSION" 
$build = "$env:VER_BUILD"
$hash = "$env:VER_HASH"
$checksum = "$env:SHA256_CHECKSUM" 

$dirName = "$version%2B$build.$hash"
$fileName = "cortex-code-cli-$dirName-x86_64.msi"
$url = "https://sfc-repo.snowflakecomputing.com/cortex-code-cli/windows_amd64/$dirName/$fileName"

Write-Host "Installing Snowflake Cortex Code version $version..."

Install-ChocolateyPackage `
  -PackageName 'snowflake-cortex-code' `
  -FileType 'msi' `
  -SilentArgs '/qn /norestart' `
  -Url $url `
  -Checksum $checksum `
  -ChecksumType 'sha256'
