# PR-Metrics

Contains the (sub-)datasets used for the statistical analysis

## Files

`extracted_dataset` : the sub-dataset (in csv and Json format) created to answer the first 2 research questions
`Spring-boot_with_authors` : contains the data extracted from the PR of the Spring-boot project, with the additions of the username of the aothor of the PR and of each comment

## Keys of the extracted dataset

| Field | Type | Description                                                             |
| :--- | :--- |:------------------------------------------------------------------------|
| `Polarity_median` | `int` | Median value of polarities of the messages of PR discussion threads                     |
| `Polarity_mean` | `int` |   Mean value of polarities of the messages of PR discussion threads |
| `Polarity_mode` | `int` | Mode value of polarities of the messages of PR discussion threads                                    |
| `PR_nb_comments` | `int` | Number of comments in PR discussion threads                                                                                                                           |
| `PR_state` | `int` | State of PR (merged : 1, open : 0, closed : -1)                          |
| `lines_added` | `int` | Number of lines added by PR                |
| `lines_removed` | `int` | Number of lines removed by PR  
| `modified_files` | `int` | Number of modified files by PR
| `modified_classes` | `int` | Number of modified classes by PR
| `class_loc` | `int` |   Median value of number of lines of code added per class
| `class_cboModified` | `int` | Median value of cboModfied of classes
| `class_wmc` | `int` | Median value of cyclomatic complexity of classes
| `class_lcom*` | `int` | Median value of lcom* of classes
| `total_methods_qtt` | `int` | Median value of number of methods inside classes
| `method_loc` | `int` | Median value of number of lines of code added per method
| `method_cboModified` | `int` |  Median value of cboModfied of methods
| `method_wmc` | `int` |  Median value of cyclomatic complexity of methods
| `parameters_qtt` | `int` | Median value of number of parameters per method
---