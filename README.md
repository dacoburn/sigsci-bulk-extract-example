# sigsci-bulk-extract-example

This script is based on the [Bulk Extract](https://docs.signalsciences.net/developer/extract-your-data/#python) example Script from Signal Sciences. It has been converted to use API Tokens and offers a few more formatting options then the default one. One of the main advantages is being able to specify the delta time period being pulled instead of an hour period and an option to write out to a log file.

## Usage

`python sigsci-bulk-extract.py`

## Configuration Options

The configuration options can either be specified in the script or as Environment Variables.

| Setting | Environment Variable Format | Default Value | Description |
|---------|-----------------------------|---------------|-------------|
| email | SIGSCI_EMAIL | `user@email.com` | email address/login name for the Signal Sciences Dashboard |
| api_token | SIGSCI_API_TOKEN | `REPLACE_ME` | API Token associated with the e-mail for logging into the Signal Sciences Dashboard |
| corp_name | SIGSCI_CORP_NAME | `REPLACE_ME` | Corp API name for the SigSci Corp you have access to |
| site_name | SIGSCI_SITE_NAME | `REPLACE_ME` | The API Name for the SigSci site you would like to pull data from |
| delta_in_minutes | SIGSCI_DELTA_IN_MINUTES | `10` | The period of time you would like to pull data from in minutes |
| pretty | SIGSCI_PRETTY | `false` | This option is whether to print the JSON on a single line or multi line but easier to read format |
| single_object | SIGSCI_SINGLE_OBJECT | `false` | This option determines whether to print all of the requests as a single object in the format of `{"data": []}` or as a single request per line |
| log_file | SIGSCI_LOG_FILE | `sigsci_results.json` | Log file name to write results out to |
