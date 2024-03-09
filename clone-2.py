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
        print(f"Error executing command: {command}\nError message: {e.stderr.decode()}")
        return False, e.stderr.decode()

# Iterates through each subdirectory in the specified directory
for subdir in next(os.walk(base_directory))[1]:
    subdir_path = os.path.join(base_directory, subdir)
    xml_files = glob.glob(os.path.join(subdir_path, '*.xml'))
    if xml_files:
        filepath = xml_files[0]
        tree = ET.parse(filepath)
        root = tree.getroot()

        student_name = root.find('name').text
        url = root.find('repositoryurl').text
        name = root.find('repositoryname').text
        hash_ = root.find('lastcommithash').text
        matnr = root.find('matrikelnummer').text

        print(f"Cloning {student_name} ({matnr}) Repository: {url} ({name})...")

        # Checks if the repository directory already exists
        repo_path = os.path.join(subdir_path, f"{name}")
        if os.path.exists(repo_path):
            print(f"Repository {name} for {student_name} already cloned. Skipping.\n")
            continue

        success, err = run_command(f"git clone {url}", cwd=subdir_path)
        if not success:
            print(f"Error, cloning failed - {err}\n")
            continue

        run_command(f"git checkout {hash_}", cwd=repo_path)

        print(f"Repo von {student_name}: {name} ({url}) successfully processed\n")