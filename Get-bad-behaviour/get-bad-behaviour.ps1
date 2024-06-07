# aware portal env variables
$AWARE_TOKEN = $env:AWARE_TOKEN
$ACCOUNT_NUMBER = $env:ACCOUNT_NUMBER

# Azure env variables
$ACCESS_SECRET = $env:ACCESS_SECRET
$AZURE_APP_ID = $env:AZURE_APP_ID
$TENANT_ID = $env:TENANT_ID

# Email env variables
$MAIL_FROM = $env:MAIL_FROM

# Date format must be yyyy-MM-dd
$date = (Get-Date).AddDays(-1).ToString("yyyy-MM-dd")

Write-Host "Fetching data for date: $date" -ForegroundColor Green

$headers = @{
    "Content-Type"  = "application/json"
    "Authorization" = "Token $AWARE_TOKEN"
}
# Request to aware API
$URI = "https://aware.advact.ch/api/v2/recipient/firstevent/?account=$ACCOUNT_NUMBER&start_date=$date&end_date=$date"

$response = Invoke-WebRequest -Uri $URI -Headers $headers | Select-Object -Expand Content

# Query the response for the required data
$jsonContent = $response
# Convert the JSON string to a PowerShell object
$jsonArray = $jsonContent | ConvertFrom-Json

# Initialize a hashtable to hold grouped data
$groupedBySupervisor = @{}

# Loop through each item in the array
foreach ($item in $jsonArray) {
    # Check if 'first_wrong' is not empty
    if ($item.first_wrong -and $item.first_wrong.Count -gt 0) {
        $email = $item.email
        $supervisorEmail = $item.custom.supervisor
        $firstWrongScenarioName = ($item.first_wrong | Select-Object -ExpandProperty scenario_name) -join ', '
        $firstWrongEventDate = ($item.first_wrong | Select-Object -ExpandProperty event_date) -join ', '

        # Check if supervisor email already exists in the hashtable
        if (-not $groupedBySupervisor.ContainsKey($supervisorEmail)) {
            $groupedBySupervisor[$supervisorEmail] = @()
        }

        # Add details to the list for this supervisor
        $groupedBySupervisor[$supervisorEmail] += [PSCustomObject]@{
            Email                  = $email
            FirstWrongScenarioName = $firstWrongScenarioName
            FirstWrongEventDate    = $firstWrongEventDate
        }

        #check if a user doens't have a supervisor
        if ($supervisorEmail -eq "") {
            write-host "WARNING: User with email $email doesn't have a supervisor and had bad behaviour" -ForegroundColor Red
        }

        # remove hashtable of users without supervisor
        $groupedBySupervisor.Remove("")
    }

}

# Send an email to each supervisor with the details of their "user's" wrong actions
foreach ($supervisor in $groupedBySupervisor.Keys) {
    write-host "Sending email to supervisor: $supervisor"

    $htmlContent = "<h1 style='color: red; font-size: 24px;'>Daily Report of bad behavior for $date</h1>";
    $htmlContent += "<p style='font-size: 18px;'>Below is the list of users that you are the supervisor of:</p>";
    $htmlContent += "<ul style='font-family: Arial, sans-serif;'>";

    # Append details for each user under this supervisor
    foreach ($data in $groupedBySupervisor[$supervisor]) {
        $htmlContent += "<li>Email of the user: $($data.Email)<br/>"
        $htmlContent += "Scenario Name: $($data.FirstWrongScenarioName)<br/>"
        $htmlContent += "Event Date: $($data.FirstWrongEventDate)</li>"
    }
    $htmlContent += "</ul>"

    # Define the token request body
    $tokenBody = @{
        Grant_Type    = "client_credentials"
        Scope         = "https://graph.microsoft.com/.default"
        Client_Id     = $AZURE_APP_ID
        Client_Secret = $ACCESS_SECRET
    }

    # Request a token from the Microsoft Graph API
    $tokenResponse = Invoke-RestMethod -Uri "https://login.microsoftonline.com/$TENANT_ID/oauth2/v2.0/token" -Method POST -Body $tokenBody

    # Set the headers for the API request
    $headers = @{
        "Authorization" = "Bearer $($tokenResponse.access_token)"
        "Content-type"  = "application/json"
    }

    # Set the URL for sending the email
    $URLsend = "https://graph.microsoft.com/v1.0/users/$MAIL_FROM/sendMail"

    # Set the JSON body for sending the email
    $BodyJsonsend = @"
{
   "message": {
       "subject": "Daily report of bad behaviour (Phishing-Service - advact AG)",
       "body": {
           "contentType": "HTML",
           "content": "$htmlContent"
       },
       "toRecipients": [
           {
               "emailAddress": {
                   "address": "$supervisor"
               }
           }
       ]
   },
   "saveToSentItems": "true"
}
"@
    # Send the email using the Microsoft Graph API
    Invoke-RestMethod -Method POST -Uri $URLsend -Headers $headers -Body $BodyJsonsend
}
