import re
import json
import os
int_pattern = re.compile(r'\d+')
java_method_declaration = re.compile(r'(?:(?:public|private|protected|static|final|native|synchronized|abstract|transient)+\s+)+[$_\w<>\[\]\s]*')
    #r'(?:(?:public|private|protected|static|final|native|synchronized|abstract|transient)+\s+)+[$_\w<>\[\]\s]*\s+[\$_\w]+')

def get_class_files(modified_files : list) :
    modified_files_names = []
    for file in modified_files :
        filename = file.filename

        if filename.endswith(".java") :
            filename = filename.replace('/', ".")
            filename = filename.replace('.java',"")
            modified_files_names.append(filename)
            
        #else : 
        #    modified_files.remove(file)
    if len(modified_files_names) > 0 :    
        return modified_files_names
    else :
        return None
    
def get_file_paths(directory) :
    file_paths = []
    
    for file in os.listdir(directory) :
        filename = os.fsencode(file)
        if filename.endswith(b'.json') :
            file_path = os.path.join(directory, filename)
            file_paths.append(file_path)
            
    return file_paths

def get_pr_numbers(json_file) :
    repo_name = ""
    pr_nb_list = []
    with open (json_file, 'r+' ,encoding="utf8") as f :
        data = json.load(f)
        for entry in range(len(data)) :    
            message_url = data[entry]["message_url"]
            pr_num = int_pattern.search(message_url).group()
            pr_nb_list.append(int(pr_num))
            if repo_name == "" :
                split_l = str(message_url).split('/')
                repo_owner = split_l[3]
                project_name = split_l[4]
                repo_name = f"{repo_owner}/{project_name}"
       
        pr_nb_list = list(set(pr_nb_list))
        return repo_name,pr_nb_list


def get_methods_name_from_patch(modified_classes : list, modified_files) :
    """extract for each file the modified methods from patches via GH API

    Args:
        modified_classes (str): file_name of modified classes (w/ .java extension) 
        modified_files (list[FILE]): list of modified classes with (necessary to get files patch)
    """
    class_method_list = []

    for i in range(len(modified_files)) :
        file = modified_files[i]
        filename = file.filename
        sanitized_file_name = str(filename).replace('/', '.')
        sanitized_file_name = str(sanitized_file_name).replace('.java', '')
        if str(filename).endswith('.java') :
            
            file_patch = file.patch
            
            if file_patch != None : #if can't get patch from api, it is removed from diff
            
                #filename = str(filename).replace('/', '.')
                #filename = str(filename).replace('.java', '')

                class_name = sanitized_file_name
                class_methods = re.findall(java_method_declaration, file_patch)

                #remove class signature, as it does not matter here
                condition = lambda x : 'class' not in x
                class_methods = [x for x in class_methods if condition(x)]

                c_m_tuple = (class_name, class_methods)
                class_method_list.append(c_m_tuple)
            
            else :
                print(f"can't get patch for file {filename}, removed from dataset")
                modified_classes.remove(sanitized_file_name)
    return class_method_list, modified_classes
