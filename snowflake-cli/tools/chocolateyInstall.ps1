$ErrorActionPreference = 'Stop'

# Construct URL and install package
$version = "$env:CLI_VERSION"
$checksum = "$env:SHA256_CHECKSUM"
$url = "https://sfc-repo.snowflakecomputing.com/snowflake-cli/windows_x86_64/$version/snowflake-cli-$version.0-x86_64.msi"

Write-Host "Installing Snowflake CLI version $version..."

Install-ChocolateyPackage `
  -PackageName 'snowflake-cli' `
  -FileType 'msi' `
  -SilentArgs '/qn /norestart' `
  -Url $url `
  -Checksum $checksum `
  -ChecksumType 'sha256'
