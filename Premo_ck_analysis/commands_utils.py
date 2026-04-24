
import subprocess


def launch_ck_analysis(unzipped_path, output_dir) :
    """launch the CK analysis on a unzipped project
    
    Args :
        unzipped_path (str) : path to unzipped project
        output_dir (str) : directory in which the CK results are written
    """
    ck_command = f"java -jar ck\\target\\ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar \
	{unzipped_path} \
        true \
        0 \
        false {output_dir}"

    print(f"launching ck_analysis on {unzipped_path}\n")
    subprocess.run(["powershell", ck_command], shell=True)
    
def empty_bin() :
    """Runs a powershell command to clear the Bin"""
    subprocess.run(["powershell", "Clear-RecycleBin -Force"], shell=True)
    
