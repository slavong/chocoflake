$ErrorActionPreference = 'Stop'

$url = 'https://sfc-repo.snowflakecomputing.com/snowflake-cli/windows_x86_64/3.29.0/snowflake-cli-3.29.0.0-x86_64.msi'
$checksum = 'd09178125a48004c4c281b654e8ae9b8a6bf69e708a74c038346d0e8aea2c5ca'

Install-ChocolateyPackage `
  -PackageName 'snowflake-cli' `
  -FileType 'msi' `
  -SilentArgs '/qn /norestart' `
  -Url $url `
  -Checksum $checksum `
  -ChecksumType 'sha256'