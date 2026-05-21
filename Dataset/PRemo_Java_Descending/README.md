# PRemo_Java_Descending

This folder contains the entries extracted from Java projects in the [PRemo replication package](https://github.com/opus-research/sentiment-replication/). The pull requests are sorted in a descending order. Other than that, the oldest entries were removed and the remaining ones not altered.
- **PRemo.dagger_descending.json** : The pull requests from Dagger
- **PRemo.eureka_descending.json** : The pull requests from Eureka
- **PRemo.gson_descending.json** : The pull requests from Gson
- **PRemo.guava_descending.json** : The pull requests from Guava
- **PRemo.guice_descending.json** : The pull requests from Guice
- **PRemo.Hystrix_descending.json** : The pull requests from Hystrix
- **PRemo.jabref_descending.json** : The pull requests from Jabref
- **PRemo.mockito_descending.json** : The pull requests from Mockito
- **PRemo.spring-boot_descending.json** : The pull requests from Spring-boot
- **PRemo.spring-security_descending.json** : The pull requests from Spring-Security

A portion of the Pull Requests from the datasets above were used for a manual preliminary analysis performed during this thesis. The types of data used were the following :
| Field | Type | Description                                                             |
| :--- | :--- |:------------------------------------------------------------------------|
| `Dépôt` | `String` | Name of the project the PR is taken from                      |
| `N°PR` | `int` |   The number of the PR (in their project)|
| `Etat PR` | `String` | The state of acceptance of the PR                                   |
| `Type PR` | `String` | The type of operation performed by the PR (new feature, refactoring,...)                                                                                                                           |
| `Polarité message` | `String` | Sentiment of the message taken from the PR discussion thread                          |
| `Ajouts/Suppressions` | `int` | Number of lines added and removed by the PR                |
| `C.cyclomatique Avant PR - Après PR` | `int` | Cyclocmatic complexity of classes before and after the PR
| `Avertissements Avant PR - Après PR` | `int` | Number of SpotBugs warnings inside de the project before and after the PR
| `Pattern majoritaire` | `int` | Main vulnerability pattern identified by SpotBugs at a given PR
| `Bugs dans classe(s) modifiée(s)` | `int` | Number of Spotbugs warnings inside the classes of the PR (untouched + modified code)  
| `Bugs dans nouveau code` | `int` | Number of SpotBugs warnings that was found inside the new code only
---
