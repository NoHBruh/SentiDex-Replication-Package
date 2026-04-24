import os 
import json
from github import Github, Auth, RateLimitExceededException, BadCredentialsException, BadAttributeException, \
    GithubException, UnknownObjectException, BadUserAgentException

import time
import requests
from pprint import pprint

from folder_utils import *
from before_api_call_utils import get_class_files, get_file_paths, get_pr_numbers, get_methods_name_from_patch
from json_utils import add_class_content_to_json, csv_to_json, add_class_diff_to_json, add_method_content_to_json, diff_routine
from constants import BASE, HEAD, CLASS_MD 
from commands_utils import launch_ck_analysis, empty_bin
from dict_utils import get_PR_metadata, comment_routine
from pymongo import MongoClient
from info import access_token


auth = Auth.Token(access_token)



def api_call(projects_dict) :
    open(output_dataset_path, 'w')
    
    while True :
        try :
            g = Github(auth=auth, per_page=200, retry=20)
            for project in projects_dict.keys() :
                
                
                repo = g.get_repo(project)
                #data[project] = {}
                
                for pr_nb in projects_dict[project] :
                    pr = repo.get_pull(pr_nb)
                    pr_key = f'PR_{pr_nb}'
                    entry_id = f'{project}_{pr_key}'
                    
                    data = {}
                    data["_id"] = entry_id
                    data["Meta"] = {}
                    data[BASE] = {}
                    data[HEAD] = {}
                    data[CLASS_MD] = {}
                    
                    try :
                        print(g.rate_limiting)
                        print(f'Retrieving Base and Head of PR # {pr.number} of repo {repo.name}')
                        # Review Comments on the Pull requests
                        base_ref = pr.base.sha
                        head_ref = pr.head.sha
                        
                        unsanitized_comments, cleaned_comments, valence_list = comment_routine(pr)
                        
                        if cleaned_comments is None :
                            print(f"No comments in PR {pr_nb}, removing from dataset creation\n".upper())
                            del data
                            continue
                        data['original_comments'] = unsanitized_comments
                        data["cleaned_comments"] = cleaned_comments
                        data["valences"] = valence_list 

                        modified_files = pr.get_files().get_page(0)
                        
                        modified_classes = get_class_files(modified_files)
                        

                        if modified_classes is None :
                            print(f"No classes modified in PR {pr_nb}, removing from dataset creation\n".upper())
                            del data
                            continue
                       
                        data = get_PR_metadata(repo, pr, data, len(modified_classes))
                        
                        
                        modified_methods_per_class, modified_classes  = get_methods_name_from_patch(modified_classes, modified_files)
                        create_folder_path(target_directory, project, pr_key)
                        
                        #Base zip
                        base_classes_ck_results, base_methods_ck_results = get_branch_zip(target_directory, project, pr_key, base_ref, BASE)
                        data = add_class_content_to_json(base_classes_ck_results, data, modified_classes, (entry_id, BASE) )
                        data = add_method_content_to_json(base_methods_ck_results, data, modified_methods_per_class, BASE)
                        print(f"Content of BASE for PR {pr_nb} added\n")
                        
                        #Head zip
                        head_classes_ck_results, head_methods_ck_results = get_branch_zip(target_directory, project, pr_key, head_ref, HEAD)
                        data = add_class_content_to_json(head_classes_ck_results, data, modified_classes, (entry_id, HEAD) )
                        data = add_method_content_to_json(head_methods_ck_results, data, modified_methods_per_class, HEAD)
                        print(f"Content of HEAD for PR {pr_nb} added\n")
                        
                        
                        pr_path = f'{target_directory}/{project.split('/')[1]}/{pr_key}'
                        base_unzip_path = get_unzip_folder_path(f'{pr_path}/{BASE}')
                        head_unzip_path = get_unzip_folder_path(f'{pr_path}/{HEAD}')
                        
                        
                        
                        print("removing unzipped archive\n")
                        delete_folder(base_unzip_path)
                        delete_folder(head_unzip_path)
                        empty_bin()
                        
                        if (len(data[BASE]) == 0 and len(data[HEAD]) == 0) :
                            print("A problem occured during the retrieving of the CK metrics, removing entry from dataset, classes not found in BASE and HEAD")
                            del data
                            continue
                        
                        #data = add_class_diff_to_json(data, entry_id)
                        data = diff_routine(data)
                        print("class diff made ToT")
                        
                        collection.insert_one(data)
                         
                    except RateLimitExceededException as e:
                        print(e.status)
                        print('Rate limit exceeded')
                        time.sleep(300)
                        continue
                    except BadCredentialsException as e:
                        print(e.status)
                        print('Bad credentials exception')
                        break
                    except UnknownObjectException as e:
                        print(e.status)
                        print('Unknown object exception')
                        break
                    except GithubException as e:
                        print(e.status)
                        print('General exception')
                        break
                    except requests.exceptions.ConnectionError as e:
                        print('Retries limit exceeded')
                        print(str(e))
                        time.sleep(10)
                        continue
                    except requests.exceptions.Timeout as e:
                        print(str(e))
                        print('Time out exception')
                        time.sleep(10)
                        continue
                    
                     
                
                
        except RateLimitExceededException as e:
                print(e.status)
                print('Rate limit exceeded')
                time.sleep(300)
                continue
        except BadCredentialsException as e:
            print(e.status)
            print('Bad credentials exception')
            break
        except UnknownObjectException as e:
            print(e.status)
            print('Unknown object exception')
            break
        except GithubException as e:
            print(e.status)
            print('General exception')
            break
        except requests.exceptions.ConnectionError as e:
            print('Retries limit exceeded')
            print(str(e))
            time.sleep(10)
            continue
        except requests.exceptions.Timeout as e:
            print(str(e))
            print('Time out exception')
            time.sleep(10)
            continue
        break
    
    #with open(output_dataset_path, "r+") as f :
    #    json.dump(data_list, f, indent=4, sort_keys=False)
    
    
def get_branch_zip(target_dir, repo : str, pr_nb , ref, branch_type) :
    assert(branch_type in ["base", "head"])
    repo_path = f'{target_dir}/{repo.split('/')[1]}'
    output_dir = f'{repo_path}/{pr_nb}/{branch_type}'
    
         
    branch_url = f"https://api.github.com/repos/{repo}/zipball/{ref}"
    headers = {"Accept" : "application/vnd.github+json"}
    print(f"Downloading from: {branch_url}")  
    response = requests.get(branch_url, headers=headers, stream=True)
    response.raise_for_status() 
    
    print('size:', len(response.content))
    content_disposition = response.headers.get("Content-Disposition", "") 
    
    filename = content_disposition.split("=")[1] 
    
    file_path = os.path.join(output_dir, filename)
    
    save_zip_content(file_path, response)
    
            
    try : 
        unzip_path = None      
        unzip_folder(output_dir, file_path)
        
        unzip_path = get_unzip_folder_path(output_dir)
        launch_ck_analysis(unzip_path, output_dir)
        ck_class_results_path = csv_to_json(output_dir, "class.csv")
        ck_methods_results_path = csv_to_json(output_dir, "method.csv")
    except  Exception as e:
        print(f'Exception : {e}')
    
    return ck_class_results_path, ck_methods_results_path 



    
#%-------------------------------------------------------   
    
if __name__ == '__main__' :
    
    my_client = MongoClient("mongodb://localhost:27017/")
    db = my_client['PRemo_CK']
    collection = db['extracted_Dataset']
    if(collection.count_documents(filter={}) > 0) :
        collection.delete_many({})
    
    repos_prs = {}
    
    if( os.path.exists(target_directory) and len(os.listdir(target_directory)) > 0) :
        print("emptying folder from previous run")
        delete_folder(target_directory)
    
    file_paths = get_file_paths(dataset_directory)
    for path in file_paths :
        repo_name, pr_nb_list = get_pr_numbers(path)
        repos_prs[repo_name] = sorted(pr_nb_list)
    api_call(repos_prs)
