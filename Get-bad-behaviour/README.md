# Get-bad-behaviour

This script is used to notify supervisors when their subordinate triggered bad behaviour in our Phishing-Simulation Service. It scans for bad behaviour of the last day, and sends an e-mail to each supervisor with the report.

## Requirements

1. Include a custom field for the supervisor’s email in the recipient upload list for each recipient.
2. Create an Azure Application with the Microsoft Graph permission for "Mail.Send."
3. Add a Client Secret to the Azure Application.
4. An API token from aware.advact.ch and your account number.
5. Ensure access to a server with PowerShell capabilities.

## Installation

### 1. Custom Field
Please add a new row to your recipient upload to include a 'supervisor-email' for each user. If a recipient lacks a supervisor email, a warning will be generated, but the script will continue to function.

### 2. Azure Application
Can be found in the main [README.md](../README.md#azure-application-to-send-e-mails-via-graph-api)
### 3. Client Secret in Azure
Can be found in the main [README.md](../README.md#client-secret-in-azure)
### 4. aware API Token
Can be found in the main [README.md](../README.md#aware-api-token-and-acccount-number)

## Usage

### Setup Environment variables:
```
# Set as variables
$awareToken "your aware_api_token"
$ACCOUNT_NUMBER = "your_aware_account_number"
$ACCESS_SECRET = "your_access_secret_from_the_azure_application"
$AZURE_APP_ID = "your_azure_app_id"
$TENANT_ID = "your_tenant_id"
$MAIL_FROM = "azure_account_email"

# Load the variables into enviorement
$env:AWARE_TOKEN = $AWARE_TOKEN
$env:ACCOUNT_NUMBER = $ACCOUNT_NUMBER
$env:ACCESS_SECRET = $ACCESS_SECRET
$env:AZURE_APP_ID = $AZURE_APP_ID
$env:TENANT_ID = $TENANT_ID
$env:MAIL_FROM = $MAIL_FROM
```
After setting up the environment variables, you can start the script in powershell as follows:
```
.\get-bad-behaviour.ps1
```
We recommend running this script daily to gather data from the previous day.
