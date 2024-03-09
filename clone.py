import argparse
import os
import xml.etree.ElementTree as ET
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-dir', help='directory of xml files', required=True)
parser.add_argument('-remove', help='flag to remove xml file after clone', action='store_true')
args = parser.parse_args()

xml_directory = args.dir
remove_afterwards = args.remove

# Iterates through all "abgabe_*.xml" files
for filepath in glob.glob(os.path.join(xml_directory, 'abgabe_*.xml')):
    tree = ET.parse(filepath)
    root = tree.getroot()

    student_name = root.find('name').text
    url = root.find('repositoryurl').text
    name = root.find('repositoryname').text
    hash_ = root.find('lastcommithash').text
    matnr = root.find('matrikelnummer').text

    os.system(f"git clone {url}")
    os.system(f"cd {name} && git checkout {hash_}")
    os.system(f"cd ../")

    os.rename(name, f"{matnr}_{name}")

    print(f"Repo von {student_name}: {name} ({url})\n")

    if remove_afterwards:
        os.remove(filepath)
