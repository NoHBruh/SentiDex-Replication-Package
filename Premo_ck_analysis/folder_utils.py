import zipfile
import os
import shutil


output_dataset_path = "Dataset/PRemo_Java_ck.json"
target_directory = "Premo_ck_analysis\\projects"

dataset_directory = os.fsencode("./Dataset/PRemo_Java_Descending")




def save_zip_content(file_path, response) :
    """saves the the content of a downloaded project archive

    Args:
        file_path (str): path wherein write the zip archive
        response : github api response containing the zipball content
    """
    with open(file_path, "wb") as f:  
        print("writing content of the archive\n")
        for chunk in response.iter_content(chunk_size=8192):  
            f.write(chunk)
        print("writing done\n")


def unzip_folder (output_dir : str, folder_path : str) :
    """unzips the downloaded archive

    Args:
        output_dir (str): the directory the project is extracted to
        folder_path (str): path to the zip archive
    """
    with zipfile.ZipFile(folder_path, 'r') as f :
        print(f"unzipping folder {folder_path}\n")
        f.extractall(output_dir) 
        print("unzipping done :)\n") 
        
        
 
        
def get_unzip_folder_path(output_dir : str) :
    """gets the path of the unzipped project
    
    Args:
        output_dir : directory containing the unzipped archive
    
    Returns:
        file_path : path to the unzipped archive
    
    Note:
        the path is required to delete the unzipped archive later
    """
       
         
    for filename in os.listdir(output_dir) :
        if not str(filename).endswith((".zip", ".csv", "json")) :
            file_path = os.path.join(output_dir, filename)
            break
    return file_path

def create_folder_path(target_dir, repo:str, pr_nb : str) :
    """creates the folder paths to the Base and Head of current Pull Request

    Args:
        target_dir (_type_): directory that will contain the base and head folders of the PR
        repo (str): repository name
        pr_nb (str): number of current Pull Request
    """
    repo_target = f'{target_dir}/{repo.split('/')[1]}/{pr_nb}'
    os.makedirs(f'{repo_target}/base', exist_ok=True)
    os.makedirs(f'{repo_target}/head', exist_ok=True)
    
    

def delete_folder(file_path) :
    """deletes a folder and all its children

    Args:
        file_path (str): path to the folder to delete, an unzipped archive that is
    """
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
 