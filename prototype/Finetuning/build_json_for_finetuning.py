from datetime import datetime
import json
import os
from Finetuning.Objects_map import *
from Consts.consts import *
from Consts.agent_code_writer_consts import *
from Consts.agent_disassembler_consts import *
from Consts.agent_assembler_consts import *
from Utils.string_utils import *
from Utils.file_utils import *
from Utils.model_utils import *

json_dir = "Finetuning\Json_Files"
examples_for_training_dir = "Finetuning\Example_For_Training"
description_files_dir = f"{examples_for_training_dir}\Part_Descriptions"
code_files_dir = f"{examples_for_training_dir}\Code_Examples"
full_program_files_dir = f"{examples_for_training_dir}\Full_Programs"

def read_description_file_and_split_parts_by_double_enter(file_name):
    try:
        content = get_file_content(description_files_dir, file_name)

        # Split the content by double row enters
        result = content.split('\n\n')

        return result
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return []


def get_code_as_string(file_name):
    file_path = os.path.join(code_files_dir, file_name + ".py")
    print(file_path)
    with open(file_path, 'r') as file:
        code_content = file.read()
    return code_content


def create_code_writer_json_file(system_message, objects):
    data_array = []
    for object_ in objects:
        object_parts = read_description_file_and_split_parts_by_double_enter(
            object_.file_name)

        for object_part in object_parts:
            data = {MESSAGES: []}
            part_description = object_.description + "\n" + object_part
            part_name = get_text_before_colon(object_part)
            part_code = get_code_as_string(
                object_.file_name + "\\" + part_name)

            message = {ROLE: USER, CONTENT: part_description}
            data[MESSAGES].append(message)

            assistant_message = {ROLE: ASSISTANT, CONTENT: part_code}
            data[MESSAGES].append(assistant_message)

            system_message_obj = {ROLE: SYSTEM, CONTENT: system_message}
            data[MESSAGES].insert(0, system_message_obj)
            data_array.append(data)

    os.makedirs(json_dir, exist_ok=True)

    formatted_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    json_file_path = os.path.join(
        json_dir, f"code_writer_finetuning_{formatted_string}.jsonl")
    with open(json_file_path, 'w') as json_file:
        for data in data_array:
            json.dump(data, json_file)  # , indent=4
            json_file.write("\n")

    print(f"JSON file created at: {json_file_path}")


def create_disassembler_json_file(system_message, objects):
    data_array = []
    for object_ in objects:
        data = {MESSAGES: []}
        parts_description = get_file_content(description_files_dir, object_.file_name)

        message = {ROLE: USER, CONTENT: object_.description}
        data[MESSAGES].append(message)

        assistant_message = {ROLE: ASSISTANT, CONTENT: parts_description}
        data[MESSAGES].append(assistant_message)

        system_message_obj = {ROLE: SYSTEM, CONTENT: system_message}
        data[MESSAGES].insert(0, system_message_obj)
        data_array.append(data)

    os.makedirs(json_dir, exist_ok=True)

    formatted_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    json_file_path = os.path.join(
        json_dir, f"disassembler_finetuning_{formatted_string}.jsonl")
    with open(json_file_path, 'w') as json_file:
        for data in data_array:
            json.dump(data, json_file)  # , indent=4
            json_file.write("\n")

    print(f"JSON file created at: {json_file_path}")

def create_assembler_json_file(system_message, objects):
    data_array = []
    for object_ in objects:        
        all_codes = create_string_with_all_parts_code_from_dir(object_.description, object_.file_name)

        full_program = get_file_content(full_program_files_dir,f"{object_.file_name}.py")
        data = {MESSAGES: []}

        system_message_obj = {ROLE: SYSTEM, CONTENT: system_message}
        data[MESSAGES].append(system_message_obj)

        message = {ROLE: USER, CONTENT: all_codes}
        data[MESSAGES].append(message)

        assistant_message = {ROLE: ASSISTANT, CONTENT: full_program}
        data[MESSAGES].append(assistant_message)

        data_array.append(data)  

    os.makedirs(json_dir, exist_ok=True)

    formatted_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    json_file_path = os.path.join(
        json_dir, f"assembler_finetuning_{formatted_string}.jsonl")
    with open(json_file_path, 'w') as json_file:
        for data in data_array:
            json.dump(data, json_file)  # , indent=4
            json_file.write("\n")

def build_code_writer_finetuning_file():
    create_code_writer_json_file(CODE_WRITER_SYSTEM_MESSAGE, OBJECTS_TO_TRAIN_CODE_WRITER)


def build_disassembler_finetuning_file():
    create_disassembler_json_file(DISASSEMBLER_SYSTEM_MESSAGE, OBJECTS_TO_TRAIN_DISSASSEMBLER)

def build_assembler_finetuning_file():
    create_assembler_json_file(ASSEMBLER_SYSTEM_MESSAGE, OBJECTS_TO_TRAIN_FULL_PROGRAM)


