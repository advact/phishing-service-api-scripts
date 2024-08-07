# Get-open-elearning

This script is used to notify supervisors when their subordinate has an open E-Learning course in our advact Learn. It scans for open E-Learnings of the last day, and sends an e-mail to each supervisor with the report.

## Requirements

1. Include a custom field for the supervisor’s email in the recipient upload list for each recipient.
2. Create an Azure Application with the Microsoft Graph permission for "Mail.Send."
3. Add a Client Secret to the Azure Application.
4. An API token from aware.advact.ch and your account number.
5. Ensure access to a server with PowerShell capabilities.

## Installation

### 1. Custom Field
Please add a new row to your recipient upload to include a 'supervisor-email' for each user. If a recipient lacks a supervisor email, a warning will be generated, but the script will continue to function.

### Azure Application to send E-Mails via graph API
Navigate to your Azure Portal and create a new App registration and add the necessary API Permissions:
![Azure_API_Permissions](../screenshots/azure_api_permissions.png)
Remember to **grant admin consent**.

This documentation may be helpful: <br>
https://woshub.com/send-email-microsoft-graph-api-powershell/


### Client Secret in Azure
Navigate to Certificates & Secrets and create a new client secret. Be sure to save the **value** of the newly created secret.
![Azure_API_Permissions](../screenshots/azure_client_secrets.png)

If environment variables are used in one of the scripts they will always be called with the prefix:
```
$env:ACCESS_SECRET
$env:AZURE_APP_ID
$env:TENANT_ID
$env:MAIL_FROM
```

### aware API Token and Acccount Number
To create a new API Token in our application navigate to [aware.advact.ch](https://aware.advact.ch/) and log in. Next, navigate to 'API Settings' and create a new token. To retrieve your account number, select an endpoint; you will then see your account number displayed in the example request.:
![aware_api_settings](../screenshots/aware_api.png)
Be sure to just copy the number for the Variables used in the script. If environment variables are used in one of the script they will always be called with the prefix:
```
$env:AWARE_TOKEN
$env:ACCOUNT_NUMBER
```

## Usage

### Setup Environment variables:
```
# Set as variables
$AWARE_TOKEN "your_aware_api_token"
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
.\get-open-elearning.ps1
```
We recommend running this script daily to gather data from the previous day.
