# Script to upload recipients list to the awareness portal using the REST API

$fileName = '<upload.csv>' #Replace with your upload file
$filePathName = '<C:\path\to\directory\>' + $fileName #replace with path to directory of uploadfile
$fileEncoded = Get-Content $filePathName -Encoding UTF8 -Raw
$fileEncoded = [System.Text.Encoding]::UTF8.GetBytes($fileEncoded)
$fileEncoded = [System.Convert]::ToBase64String($fileEncoded)
# aware portal env variables
$AWARE_TOKEN = $env:AWARE_TOKEN
$ACCOUNT_NUMBER = $env:ACCOUNT_NUMBER

$uri = 'https://aware.advact.ch/api/v0/recipientupload/new/'

$body = @{
'account'=$ACCOUNT_NUMBER
'import_file_name'=$fileName
'import_file'='data:text/csv;base64,'+$fileEncoded
} | ConvertTo-Json

$headers = @{
'Accept'='application/json'
'Authorization'='Token ' + $AWARE_TOKEN
'Content-Type'='application/json'
}
#use of proxy is possible, just uncomment if needed
#$proxy = [System.Net.WebRequest]::GetSystemWebProxy().GetProxy($uri)

$Parameters = @{
Method = 'POST'
Uri = $uri
Headers = $headers
Body = $body
#Proxy = $proxy
#ProxyUseDefaultCredentials = $true
}

Invoke-WebRequest @Parameters