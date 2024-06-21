# automated-recipient-upload
This is a simple script that automates the process of uploading recipient lists. It reads a CSV file and uploads the recipients to our application.

## Requirements
1. An API token from aware.advact.ch and your account number.
2. Ability to execute Powershell.

## Installation

### aware API Token and Acccount Number
To create a new API Token in our application navigate to [aware.advact.ch](https://aware.advact.ch/) and log in. Next, navigate to 'API Settings' and create a new token. To retrieve your account number, select an endpoint; you will then see your account number displayed in the example request.:
![aware_api_settings](../screenshots/aware_api.png)
Be sure to only copy the number for the account number. If environment variables are used in one of the script they will always be called with the prefix:
```
$env:AWARE_TOKEN
$env:ACCOUNT_NUMBER
```

## Usage

### Setup Environment variables:
```
# Set as variables
$awareToken = "your aware_api_token"
$ACCOUNT_NUMBER = "your_aware_account_number"

# Load the variables into enviorement
$env:AWARE_TOKEN = $AWARE_TOKEN
$env:ACCOUNT_NUMBER = $ACCOUNT_NUMBER
```
### define the path to the csv file

In the main.ps1 file, you need to define the path to the csv file in Line 3 and 4.

After defining the environment variables and path, you can start the script in powershell as follows:
```
.\main.ps1
```
