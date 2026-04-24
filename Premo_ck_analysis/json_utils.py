import json
import csv
from constants import BASE, HEAD, CLASS_MD, ADDED, REMOVED

needed_class_metrics = ["loc", "wmc", 'cboModified', 'lcom*', 'totalMethodsQty', 'staticMethodsQty',
                  'publicMethodsQty', 'privateMethodsQty', 'protectedMethodsQty', 'defaultMethodsQty',
                  'visibleMethodsQty', 'abstractMethodsQty', 'finalMethodsQty', 'synchronizedMethodsQty']

needed_method_metrics = ["loc", "cboModified", "wmc", 'parametersQty']

unwanted_in_all_key = needed_class_metrics + ["Was_added", "Was_modified", "Was_removed"]

def csv_to_json(output_dir : str, filename : str) :
    csv_path = f'{output_dir}/{filename}'
    filename_no_extension = filename.split(".")[0]
    json_path = f'{output_dir}/{filename_no_extension}.json'
    
    with open(csv_path, mode='r', newline='', encoding='utf-8') as csvfile:
        data = list(csv.DictReader(csvfile))

    with open( json_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    print("ck result converted to json\n")
    return json_path
    

def add_class_content_to_json(ck_result_path : str, data_dict : dict, modified_classes : list, pj_infos : tuple) :
    with open (ck_result_path, 'r+' ,encoding="utf8") as f :
        data = json.load(f)
    
    project_name = pj_infos[0] # is the ID
    
    branch = pj_infos[1]
        
    for entry in range(len(data)) :
        
        #if(len(modified_classes) == 0) :
        #    return data_dict
        
        class_name = data[entry]["class"]
        
        for mod_file in modified_classes : 
            needed_metrics_dict = {}
            
            if str(mod_file).endswith(class_name) :
                del data[entry]["file"]
                del data[entry]["class"]
                del data[entry]["type"]
                class_name = str(class_name).replace(".", '-')
                for metric in data[entry].keys():
                    if (metric in needed_class_metrics) :
                    
                        val = data[entry][metric]
                        if(val == "NaN") :
                            val = 0
                        else :
                            val = int(val) if val.isdigit() else float(val)
                        
                        needed_metrics_dict[metric] = val
                        
                    

                data_dict[branch][class_name] = {}
                data_dict[branch][class_name] = needed_metrics_dict
                    
                break
        
    return data_dict


def add_method_content_to_json(ck_result_path : str, data_dict : dict, modif_method_per_class : list, branch : str) :
    with open (ck_result_path, 'r+' ,encoding="utf8") as f :
        data = json.load(f)
      
    for entry in range(len(data)) :
        needed_metrics_dict = {}
        class_name_file = data[entry]["class"]
        #needed_metrics_dict["class"] = class_name_file
        
        
        #On saute l'entrée si la classe n'a pas été modifiée par la PR
        if not any(str(item[0]).endswith(class_name_file) for item in modif_method_per_class) :
            continue
        
        method_name_file = data[entry]['method']
        method_name_pure = method_name_file.split('/')[0]
        
        
        #On vérifie si la méthode a été modifiée par la PR
        for item in modif_method_per_class :
            if any(str(mtd).endswith(method_name_pure) for mtd in item[1]) :
                
                #Ici a priori on a que les dico pour les méthodes du patch :thumbsup
                
                for metric in needed_method_metrics :
                    val = data[entry][metric]

                    if (val == "NaN") :
                        val = 0
                    else :
                        val = int(val) if val.isdigit() else float(val)

                    needed_metrics_dict[metric] = val
               
                #metrics_method_list.append(needed_metrics_dict)
        class_name_file = str(class_name_file).replace('.', '-')
        if len(needed_metrics_dict.keys()) > 0 :
          
            data_dict[branch][class_name_file][method_name_pure] = needed_metrics_dict
    
    return data_dict
    
                
            
def add_class_diff_to_json(data_dict : dict, entry_id : str) :
    
    
    base_dict = data_dict[BASE]
    head_dict = data_dict[HEAD]
    
    
    base_keys = base_dict.keys()
    head_keys = head_dict.keys()
    
   
    #data_dict[project_name][pr_nb][md] = {}
    if len(head_keys) >= len(base_keys) :
        for class_name in head_keys:
            data_dict[CLASS_MD][class_name] = {}
            if class_name in base_keys : #classic Diff of classes
                data_dict[CLASS_MD][class_name]["Was_modified"] = True
                data_dict[CLASS_MD][class_name]["Was_added"] = False
                data_dict[CLASS_MD][class_name]["Was_removed"] = False
                
                base_metrics_dict = base_dict[class_name]
                head_metrics_dict = head_dict[class_name]
                for metric in base_metrics_dict.keys() :
                    if isinstance(base_metrics_dict[metric], (int, float)) :
                        diff = head_metrics_dict[metric] - base_metrics_dict[metric]
                        data_dict[CLASS_MD][class_name][metric] = diff
                    
                    else : #iterate through methods dict #TODO CHECKER LE DIFF DES METHODES
                        dico = {}
                        for mtd_metric in  base_metrics_dict[metric].keys() :
                            m_diff = head_metrics_dict[metric][mtd_metric] - base_metrics_dict[metric][mtd_metric]
                            dico[mtd_metric] = m_diff
                        data_dict[CLASS_MD][class_name][metric] = dico
                        
            else : #The file was added by the PR
                
                data_dict[CLASS_MD][class_name]["Was_modified"] = False
                data_dict[CLASS_MD][class_name]["Was_added"] = True
                data_dict[CLASS_MD][class_name]["Was_removed"] = False
                diff = head_dict[class_name]
                for metric in diff.keys() :
                    if isinstance(diff[metric], (int, float)) :
                        data_dict[CLASS_MD][class_name][metric] = diff[metric]

                    else : #get methods metrics
                        dico = {}
                        dico["Was_modified"] = False
                        dico["Was_added"] = True
                        dico["Was_removed"] = False
                        for m in diff[metric].keys() :
                            d = diff[metric][m]
                            dico[m] = d
                            
                        data_dict[CLASS_MD][class_name][metric] = dico
                        
                        
    #class file was deleted in PR (base > head)
    else:
        for class_name in base_keys :
            data_dict[CLASS_MD][class_name] = {}
            if class_name in head_keys : #Classic Diff
                data_dict[CLASS_MD][class_name]["Was_modified"] = True
                data_dict[CLASS_MD][class_name]["Was_added"] = False
                data_dict[CLASS_MD][class_name]["Was_removed"] = False
                base_metrics_dict = base_dict[class_name]
                head_metrics_dict = head_dict[class_name]
                for metric in base_metrics_dict.keys() :
                    if isinstance(base_metrics_dict[metric], (int, float)) :
                        diff = head_metrics_dict[metric] - base_metrics_dict[metric]
                        data_dict[CLASS_MD][class_name][metric] = diff
                    
                    else : #iterate through methods dict #TODO CHECKER LE DIFF DES MÉTHODES
                        base_methods_metrics = base_metrics_dict[metric].keys()
                        head_methods_metrics = head_metrics_dict[metric].keys()
                        dico = {}

                        if metric in base_metrics_dict.keys() and metric in head_metrics_dict.keys():#classic DIFF
                            dico["Was_modified"] = True
                            dico["Was_added"] = False
                            dico["Was_removed"] = False
                            for mtd_metric in base_methods_metrics :
                                
                                    
                                m_diff = head_metrics_dict[metric][mtd_metric] - base_metrics_dict[metric][mtd_metric]
                                dico[mtd_metric] = m_diff
                                
                            data_dict[CLASS_MD][class_name][metric] = dico
                            
                        elif metric not in head_metrics_dict.keys() : #method was deleted 
                            dico["Was_modified"] = False
                            dico["Was_added"] = False
                            dico["Was_removed"] = True
                            for mtd_metric in base_methods_metrics :
                                dico[mtd_metric] = m_diff
                            data_dict[CLASS_MD][class_name][metric] = dico
                            
            else : #The file was removed by the PR
                
                data_dict[CLASS_MD][class_name]["Was_modified"] = False
                data_dict[CLASS_MD][class_name]["Was_added"] = False
                data_dict[CLASS_MD][class_name]["Was_removed"] = True
                diff = head_dict[class_name]
                for metric in diff.keys() :
                    if isinstance(diff[metric], (int, float)) :
                        data_dict[CLASS_MD][class_name][metric] = diff[metric]

                    else : #get methods metrics
                        dico = {}
                        dico["Was_modified"] = False
                        dico["Was_added"] = False
                        dico["Was_removed"] = True
                        for m in diff[metric].keys() :
                            d = diff[metric][m]
                            dico[m] = d
                        data_dict[CLASS_MD][class_name][metric] = dico
            #iterate on key-value or dict for method
        #for key in data_dict[CLASS_MD][class_name].keys() :
        #    value = data_dict[CLASS_MD][class_name][key]
        #    if isinstance(value, (int,float)) :
        #        data_dict[CLASS_MD][class_name][key] = -value
        #    else :
        #        for entry in value.keys() :
        #            data_dict[CLASS_MD][class_name][key][value][entry] = -(value[entry])    
                   
 
    return data_dict


def diff_routine(data_dict ) :
    base_dict = data_dict[BASE]
    head_dict = data_dict[HEAD]
    
    base_keys = base_dict.keys()
    head_keys = head_dict.keys()
    
    all_classes = get_all_class_keys(base_keys, head_keys)
    
    for class_name in all_classes :
        base_metrics_dict = base_dict[class_name]  if class_name in base_keys else None
        head_metrics_dict = head_dict[class_name]  if class_name in head_keys else None  
        
        data_dict[CLASS_MD][class_name] = {}
        
        if class_name in base_keys and class_name in head_keys : #classic diff
            data_dict[CLASS_MD][class_name]["Was_modified"] = True
            data_dict[CLASS_MD][class_name]["Was_added"] = False
            data_dict[CLASS_MD][class_name]["Was_removed"] = False
            
            base_methods_keys = base_dict[class_name].keys()
            head_methods_keys = head_dict[class_name].keys()
            
            all_methods = get_method_per_class_keys(base_methods_keys, head_methods_keys)
            
            for metric in all_methods : #contient aussi les métriques de classes
            
                if metric in needed_class_metrics :
                    diff = head_metrics_dict[metric] - base_metrics_dict[metric]
                    data_dict[CLASS_MD][class_name][metric] = diff
                
                else : #iterate through methods dict, the "metric" key is then a method name (and a Dict)
                    data_dict[CLASS_MD][class_name][metric] = {}
                    if metric in base_methods_keys and metric in head_methods_keys : #classic Diff
                        
                        for mtd_metric in  base_metrics_dict[metric].keys() :
                            m_diff = head_metrics_dict[metric][mtd_metric] - base_metrics_dict[metric][mtd_metric]
                            data_dict[CLASS_MD][class_name][metric][mtd_metric] = m_diff
                            data_dict[CLASS_MD][class_name][metric]["Was_modified"] = True
                            data_dict[CLASS_MD][class_name][metric]["Was_added"] = False
                            data_dict[CLASS_MD][class_name][metric]["Was_removed"] = False
                    elif metric in base_methods_keys and metric not in head_methods_keys : #method was deleted
                        diff = base_dict[class_name][metric]
                        dico = {}
                        dico["Was_modified"] = False
                        dico["Was_added"] = False
                        dico["Was_removed"] = True
                        for key in diff.keys() :
                            dico[key] = diff[key]
                        data_dict[CLASS_MD][class_name][metric] = dico
                    
                    elif metric in head_methods_keys and metric not in base_methods_keys : #method was added
                        diff = head_dict[class_name][metric]
                        dico = {}
                        dico["Was_modified"] = False
                        dico["Was_added"] = True
                        dico["Was_removed"] = False
                        for key in diff.keys() :
                            dico[key] = diff[key]
                        data_dict[CLASS_MD][class_name][metric] = dico
                        
        elif class_name in head_keys and class_name not in base_keys : #class was added by PR
            data_dict = diff_added_file(data_dict, class_name, head_dict)
        
        elif class_name in base_keys and class_name not in head_keys : #class was deleted by PR
            data_dict = diff_deleted_file(data_dict, class_name, base_dict)
    
    return data_dict

def get_all_class_keys(base_keys, head_keys) :
    all_classes = []
    for k in base_keys :
        all_classes.append(k)
    for k in head_keys :
        if k not in all_classes :
            all_classes.append(k)
        
    return all_classes

def get_method_per_class_keys(base_methods_keys, head_methods_keys) :
    all_methods = []
    for k in base_methods_keys :
        all_methods.append(k) 
            
    for k in head_methods_keys :
        if k not in all_methods :
            all_methods.append(k)
    
    return all_methods
    
def diff_added_file(data_dict, class_name, head_dict) :
    data_dict[CLASS_MD][class_name]["Was_modified"] = False
    data_dict[CLASS_MD][class_name]["Was_added"] = True
    data_dict[CLASS_MD][class_name]["Was_removed"] = False
    diff = head_dict[class_name]
    for metric in diff.keys() :
        if isinstance(diff[metric], (int, float)) :
            data_dict[CLASS_MD][class_name][metric] = diff[metric]
        else : #get methods metrics
            dico = {}
            dico["Was_modified"] = False
            dico["Was_added"] = True
            dico["Was_removed"] = False
            for m in diff[metric].keys() :
                d = diff[metric][m]
                dico[m] = d
                
            data_dict[CLASS_MD][class_name][metric] = dico
    return data_dict

def diff_deleted_file(data_dict, class_name, base_dict) :
    data_dict[CLASS_MD][class_name]["Was_modified"] = False
    data_dict[CLASS_MD][class_name]["Was_added"] = False
    data_dict[CLASS_MD][class_name]["Was_removed"] = True
    diff = base_dict[class_name]
    for metric in diff.keys() :
        if isinstance(diff[metric], (int, float)) :
            data_dict[CLASS_MD][class_name][metric] = diff[metric]
        else : #get methods metrics
            dico = {}
            dico["Was_modified"] = False
            dico["Was_added"] = True
            dico["Was_removed"] = False
            for m in diff[metric].keys() :
                d = diff[metric][m]
                dico[m] = d
                
            data_dict[CLASS_MD][class_name][metric] = dico
    return data_dict