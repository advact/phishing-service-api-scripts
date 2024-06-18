### aware API Token and Acccount Number
To create a new API Token in our application navigate to [aware.advact.ch](https://aware.advact.ch/) and log in. Next, navigate to 'API Settings' and create a new token. To retrieve your account number, select an endpoint; you will then see your account number displayed in the example request.:
![aware_api_settings](screenshots/aware_api.png)
Be sure to just copy the number for the Variables used in the script. If environment variables are used in one of the script they will always be called with the prefix:
```
$env:AWARE_TOKEN
$env:ACCOUNT_NUMBER
```