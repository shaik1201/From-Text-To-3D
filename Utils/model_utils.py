import os
from Utils.file_utils import *
json_dir = "Finetuning\Json_Files"
examples_for_training_dir = "Finetuning\Example_For_Training"
description_files_dir = f"{examples_for_training_dir}\Part_Descriptions"
code_files_dir = f"{examples_for_training_dir}\Code_Examples"
full_program_files_dir = f"{examples_for_training_dir}\Full_Programs"

def create_string_with_all_parts_code(object_name,part_codes):
        # Create string with all parts
    all_codes = f"Object: {object_name}"
    for i, part_code in enumerate(part_codes):
        all_codes = f"{all_codes}\n\npart {i+1}\n{part_code}"
    return all_codes

def create_string_with_all_parts_code_from_dir(object_name, object_part_dir):
    objects_functions_dir = f"{code_files_dir}\{object_part_dir}"
    list_files = os.listdir(objects_functions_dir)
    all_codes = f"Object: {object_name}"
    for i, filename in enumerate(list_files):
        content = get_file_content(objects_functions_dir,filename)
        all_codes = f"{all_codes}\n\npart {i+1}\n{content}"
    return all_codes