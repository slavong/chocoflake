# chocoflake

Chocolatey packages for Snowflake tools.

## Packages

- [Snowflake CLI](snowflake-cli/README.md) — [Chocolatey package](https://community.chocolatey.org/packages/snowflake-cli)
- [Cortex Code CLI](cortex-code-cli/README.md) — [Chocolatey package](https://community.chocolatey.org/packages/cortex-code-cli)
- [Snowflake ODBC Driver](snowflake-odbc-driver/README.md) — [Chocolatey package](https://community.chocolatey.org/packages/snowflake-odbc-driver)

## Install a package

Install [Chocolatey](https://chocolatey.org/install) first if it is not already installed. Open PowerShell as Administrator, then install the package by its Chocolatey ID:

```powershell
choco install snowflake-cli
choco install cortex-code-cli
choco install snowflake-odbc-driver
```

Run only the command for the package you want. To install a specific version, add `--version <VERSION>` (for example, `choco install snowflake-cli --version 3.29.0`). Visit the linked Chocolatey package pages above to see available versions and package details.

## Check upstream versions

Before updating a package, check Snowflake's official download indexes for the latest available upstream version and installer files:

| Tool | Snowflake download index |
| --- | --- |
| Snowflake CLI (Windows x86_64) | [snowflake-cli/windows_x86_64](https://sfc-repo.snowflakecomputing.com/snowflake-cli/windows_x86_64/) |
| Cortex Code CLI (Windows AMD64) | [cortex-code-cli/windows_amd64](https://sfc-repo.snowflakecomputing.com/cortex-code-cli/windows_amd64/) |
| Snowflake ODBC Driver (Windows 64-bit) | [odbc/win64](https://sfc-repo.snowflakecomputing.com/odbc/win64/) |

These are the upstream indexes used by the package version/checksum helper scripts. Check the corresponding [Chocolatey package pages](#packages) as well to confirm which versions have been published for installation.

## Build environment

The package build instructions use Chocolatey 2.7.4 and PowerShell 7.6.6.
