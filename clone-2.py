import argparse
import os
import xml.etree.ElementTree as ET
import glob
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-dir', help='directory of student folders', required=True)
args = parser.parse_args()

base_directory = args.dir

def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, result.stdout.decode()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip()
        print(f"**Error:** {command}: {error_message}")
        return False, error_message

# Iterates through each subdirectory in the specified directory
for subdir in next(os.walk(base_directory))[1]:
    subdir_path = os.path.join(base_directory, subdir)
    xml_files = glob.glob(os.path.join(subdir_path, '*.xml'))
    if xml_files:
        filepath = xml_files[0]
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"**Error:** XML parsing error in file {filepath}: {e}")
            continue

        student_name_element = root.find('name')
        if student_name_element is None:
            print(f"**Error:** 'name' tag not found in {filepath}. Skipping.\n")
            continue
        student_name = student_name_element.text

        url_element = root.find('repositoryurl')
        if url_element is None:
            print(f"**Error:** 'repositoryurl' tag not found in {filepath}. Skipping.\n")
            continue
        url = url_element.text

        name_element = root.find('repositoryname')
        if name_element is None:
            print(f"**Error:** 'repositoryname' tag not found in {filepath}. Skipping.\n")
            continue
        name = name_element.text

        hash_element = root.find('lastcommithash')
        if hash_element is None:
            print(f"**Error:** 'lastcommithash' tag not found in {filepath}. Skipping.\n")
            continue
        hash_ = hash_element.text

        matnr_element = root.find('matrikelnummer')
        if matnr_element is None:
            print(f"**Error:** 'matrikelnummer' tag not found in {filepath}. Skipping.\n")
            continue
        matnr = matnr_element.text

        print(f"Cloning {student_name} ({matnr}) Repository: {url} ({name})...")

        # Checks if the repository directory already exists
        repo_path = os.path.join(subdir_path, f"{name}")
        if os.path.exists(repo_path):
            print(f"Repository {name} for {student_name} already cloned. Skipping.\n")
            continue

        success, err = run_command(f"git clone {url}", cwd=subdir_path)
        if not success:
            print(f"**Error:** Cloning failed - {err}\n")
            continue

        # Check if cloned folder name matches repository name in XML file
        clone_output_dir = url.split('/')[-1]
        if(clone_output_dir.endswith('.git')):
            clone_output_dir = clone_output_dir[:-4] # Removes .git extension
        
        actual_repo_path = os.path.join(subdir_path, clone_output_dir)

        if clone_output_dir != name:
            print(f"**Warning:** Cloned repository folder name '{clone_output_dir}' does not match the repository name '{name}' in the XML file. Renaming folder name to XML name.")
            os.rename(actual_repo_path, repo_path)

        run_command(f"git checkout {hash_}", cwd=repo_path)

        print(f"Repo von {student_name}: {name} ({url}) successfully processed.\n")