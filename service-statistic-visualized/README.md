# service-statistic-visualized
This script retrieves all statistics data from each custom field for a selected service and visualizes them in bar chars. This allows you to determine which custom field performs the best, among other insights. The images are saved in the same directory as the script. Users can store a configuration file. The images are saved according to the corresponding custom field names. The bar chars could look like that: 
![Example screenshot](screenshots/example.png)

## Requirements

1. An API token from aware.advact.ch and your account number.
2. Ability to execute Python3.

## Installation

### 1. Get aware API Token and account number
Can be found in the main [README.md](../README.md#aware-api-token-and-acccount-number)

## Usage

```
pip install requests pandas matplotlib seaborn
```

Or you can use:

```
pip install -r requirements.txt
```
After that you will be able to launch the script
```
python3 main.py
```