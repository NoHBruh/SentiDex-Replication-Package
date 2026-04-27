# SentiDex-Replication-Package
Replication Package of the SentiDex Master's thesis
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![PowerShell](https://img.shields.io/badge/PowerShell-%235391FE.svg?style=for-the-badge&logo=powershell&logoColor=white)

This package contains a script of automated extraction of CK metrics in Java projects Pull Requests using GitHub API. A sentiment analysis is conducted on the conversation comments of the Pull Requests. The latter are retrieved from the [PRemo Dataset](https://github.com/opus-research/sentiment-replication/) by parsing the Pull Request numbers from the message link URLs.
## Content

- **CK** : folder containing an executable JAR snapshot of [Mauricio Aniche's CK tool](https://github.com/mauricioaniche/ck), used for metrics extraction in Java projects. You just need to unzip the CK folder to the project root
- **Dataset** : contains the different datasets used and produced
    - PRemo_Java_Descending : extracted pull requests per Java project from the [PRemo Dataset](https://github.com/opus-research/sentiment-replication/)
- **PRemo_ck_analysis** : contains the main script and utils files of automated ck metrics extraction from projects pull requests using Github API

## Requirements
- [**Python**](https://www.python.org/) : 3.10+
- [**MongoDB**](https://www.mongodb.com/try/download/community) (optionnal but recommended : [**Mongo Compass**](https://www.mongodb.com/products/tools/compass))
- Github API token :
        To create a token (if you don't already have one), go to your Github account settings, then ``Developper Seetings > Personal acces tokens > Fine-grained tokens`` then create a token. Save it somewhere, as you will not see its value again otherwise. 

    ### Libraries
    - [Pygithub](https://pygithub.readthedocs.io/en/stable/) : to facilitate API calls
    - [Pymongo](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/) : Mongo client in Python, used to instantiate and insert results inside a database
    - [vaderSentiment](https://vadersentiment.readthedocs.io/en/latest/pages/installation.html) : library for sentiments analysis. used on PR converesation comments

    To install all the needed dependencies, start by cloning the repository, then set up a virtual environnement, activate it and launch at the repo's root the following command : ```pip install -r requirements.txt```


## Potential Issues

For Windows users, when trying to unzip projects when running the script, you may encounter a ``FileDoesNotExistException``. It is probably due to the file path limitation on Windows (260 characters limit), you'll have to disable it when installing Python or disable it in your Registry Editor (pc must be rebooted afterwards). 