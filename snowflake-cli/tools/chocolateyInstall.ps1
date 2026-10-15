$ErrorActionPreference = 'Stop'

# Validate that the environment variables are set

# Only set CLI_VERSION if it is not already defined or is empty
if (-not $env:CLI_VERSION) {
    Write-Host "Using existing CLI_VERSION: $env:CLI_VERSION" -ForegroundColor Green
# use env var set by chocolatey
} elseif ($env:ChocolateyPackageVersion) {
    $env:CLI_VERSION =$env:ChocolateyPackageVersion
    Write-Host "Using existing ChocolateyPackageVersion: $env:CLI_VERSION" -ForegroundColor Green
# Check if running in GitHub Actions with a tag/ref name available
} elseif ( ($env:GITHUB_REF_NAME) {
    # Strip leading 'v' or 'V' (e.g., "v3.29.0" -> "3.29.0")
    $env:CLI_VERSION =$env:GITHUB_REF_NAME -replace '^[vV]', ''
    Write-Host "Extracted CLI_VERSION from GitHub tag ($env:GITHUB_REF_NAME): $env:CLI_VERSION" -ForegroundColor Green
# Fallback to python script to get the latest version available, if still not set
} else {
    Write-Host "CLI_VERSION not set, not specified by Chocolatey and no GitHub tag found. Fetching the latest version..." -ForegroundColor Cyan
    $env:CLI_VERSION = python get_latest_version.py
    Write-Host "Latest version found: $env:CLI_VERSION"
}

# Ensure SHA256_CHECKSUM is also set (you can do a similar check or fetch it)
if (-not $env:SHA256_CHECKSUM) {
    Write-Host "SHA256_CHECKSUM is not set. Fetching checksum for version $env:CLI_VERSION..." -ForegroundColor Cyan
    $env:SHA256_CHECKSUM = python check_snowflake_cli.py
}

# Construct URL and install package
$version = $env:CLI_VERSION
$checksum = $env:SHA256_CHECKSUM
$url = "https://sfc-repo.snowflakecomputing.com/snowflake-cli/windows_x86_64/$version/snowflake-cli-$version.0-x86_64.msi"

Write-Host "Installing Snowflake CLI version $version..."

Install-ChocolateyPackage `
  -PackageName 'snowflake-cli' `
  -FileType 'msi' `
  -SilentArgs '/qn /norestart' `
  -Url $url `
  -Checksum $checksum `
  -ChecksumType 'sha256'
