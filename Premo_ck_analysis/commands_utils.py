
import subprocess
import os

def launch_ck_analysis(unzipped_path, output_dir) :
    
    ck_command = f"java -jar ck\\target\\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar \
	{unzipped_path} \
        true \
        0 \
        false {output_dir}"

    print(f"launching ck_analysis on {unzipped_path}\n")
    subprocess.run(["powershell", ck_command], shell=True)
    
def empty_bin() :
    subprocess.run(["powershell", "Clear-RecycleBin -Force"], shell=True)
    
