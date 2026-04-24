# PRemo_CK_analysis
Contains the script and utils files

## Content
- **before_api_call_utils\.py** : contains some utils functions used before the API call routine

- **commands_utils\.py** : contains utils functions used to launch powershell commands (you can adapt the commands to run on Linux or Mac)
 
- **constants\.py** : contains constants values

- **dict_utils\.py** : contains utils functions to metadata extraction and comments sanitization
- **folder_utils\.py** : contains utils functions related to folders creation and folder paths
**info\.py** : the file wherein you should paste you Github API token (the file is inside the .gitignore). create it and add the following line ``access_token = "replace_with_your_token_value"``
- **json_utils\.py** : contains utils functions related to json file manipulation
- **main\.py** : the file to run to launch the API calls routine
vader_anamysis_utils.py : contains utils functions related to sentiment analysis of pull requests comments using VaderSentiment
