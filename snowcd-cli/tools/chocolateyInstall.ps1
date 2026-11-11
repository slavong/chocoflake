$ErrorActionPreference = 'Stop'

$version = "$env:SNOWCD_VERSION"
$checksum = "$env:SHA256_CHECKSUM"
$url = "https://sfc-repo.snowflakecomputing.com/snowcd/win64/$version/snowcd-$version-windows_x86_64.msi"

Write-Host "Installing SnowCD version $version..."

Install-ChocolateyPackage `
  -PackageName 'snowcd-cli' `
  -FileType 'msi' `
  -SilentArgs '/qn /norestart' `
  -Url $url `
  -Checksum $checksum `
  -ChecksumType 'sha256'
