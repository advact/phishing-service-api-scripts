$AWARE_TOKEN = $env:AWARE_TOKEN
$ACCOUNT_NUMBER = $env:ACCOUNT_NUMBER

$MINIMUM = Read-Host "Please enter the minimum level score"

$headers = @{
    "Content-Type"  = "application/json"
    "Authorization" = "Token $AWARE_TOKEN"
}

# Request to aware API
$URI = "https://aware.advact.ch/api/recipient/?account=$ACCOUNT_NUMBER&limit=-1&offset=0&filter=&search=&reporter_created=&active=active&start_date=&end_date="

$response = Invoke-WebRequest -Uri $URI -Headers $headers | Select-Object -Expand Content

# Query the response for the required data
$jsonContent = $response
# Convert the JSON string to a PowerShell object
$jsonArray = $jsonContent | ConvertFrom-Json

Write-Host "Those recipients have a level below" $MINIMUM
Write-Host "=============================================="
foreach ($item in $jsonArray) {
    $level = $item.level
    $recipient = $item.email

    if ($level -lt $MINIMUM) {
        Write-Host $recipient "-->" $level
        Write-Host "----------------------------------------"
        
    }
}