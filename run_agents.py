from datetime import datetime
import os
from Agents.agent_code_writer import *
from Agents.agent_disassembler import *
from Agents.agent_assembler import *
from Agents.agent_parameter_manipulator import *
from Utils.string_utils import *
from Utils.file_utils import *
from Utils.model_utils import *

main_dir = "Files_Generated_By_Agents"
full_programs_dir = f"{main_dir}/Full_Programs_Generated"
disassembler_dir = f"{main_dir}/Disassembler_Generated"
parts_functions_dir = f"{main_dir}/Parts_Functions_Generated"
time_format = "%m/%d/%Y, %H:%M:%S"

def run_all_agents(object_name):
    print(f"Recived object to generate: {object_name}")
    formatted_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    formatted_object_name = object_name.replace(" ","_")
    files_name = f"{formatted_object_name}_{formatted_time}"
    start_time = datetime.now()
    print(f"Start time: {start_time.strftime(time_format)}")
    
    object_description = run_disassembler_agent_for_prompt(object_name, files_name)

    part_codes = run_code_writer_agent_for_object(object_name,object_description,files_name)

    # Create string with all parts
    all_codes = create_string_with_all_parts_code(object_name, part_codes)

    run_full_program_agent(all_codes,files_name)
    
    # Finish - time calculation
    end_time = datetime.now()
    print(f"End time: {end_time.strftime(time_format)}")
    duration = end_time-start_time
    print(f"Total runing time: {duration} in ms: {int(duration.total_seconds() * 1000)}")
    return files_name

def run_disassembler_agent_for_prompt(object_name, files_name):
    print("------------------------------------- 1st AGENT -----------------------------------------")
    object_description = run_disassembler_agent(object_name)
    print(f"Disassembler agent finish runing result:\n{object_description}")
    print("------------------------------------------------------------------------------")

    #Save part as file
    os.makedirs(disassembler_dir, exist_ok=True)
    disassembler_file_path = os.path.join(disassembler_dir, files_name)
    with open(disassembler_file_path, 'w') as disassembler_file:
        disassembler_file.write(object_description)
    print(f"File created at: {disassembler_file_path}")
    return object_description

def run_code_writer_agent_for_object(object_name,object_description,files_name):
    print("------------------------------------- 2nd AGENT -----------------------------------------")
    object_parts = object_description.split('\n\n')
    part_codes = []
    for i, part in  enumerate(object_parts):
        part_full_description = object_name + '\n\n' + part
        part_name = get_text_before_colon(part)
        print(f"Code writer agent start runing for part {i+1} - {part_name} - prompt:\n{part_full_description}")
        part_code = run_code_writer_agent(part_full_description)
        print(f"Code writer agent finish runing for part {i+1} - {part_name} - result:\n{part_code}")
        print("------------------------------------------------------------------------------")

        #Save part code as file
        object_dir=f"{parts_functions_dir}\{files_name}"
        os.makedirs(object_dir, exist_ok=True)
        part_function_file_path = os.path.join(object_dir, f"{part_name}.py")
        with open(part_function_file_path, 'w') as part_function_file:
            part_function_file.write(part_code)
        print(f"File created at: {part_function_file_path}")

        # Append part to array of parts
        part_codes.append(part_code)
    return part_codes

def run_full_program_agent(all_codes, files_name):
    print("------------------------------------- 3rd AGENT -----------------------------------------")
    print(f"Assembler agent start runing prompt:\n{all_codes}")
    print("------------------------------------------------------------------------------")
    full_program = run_assembler_agent(all_codes)
    print(f"Assembler agent finish runing result:\n{full_program}")
    print("------------------------------------------------------------------------------")
    print("Start creating python file with full program")

    # Save full program into file
    os.makedirs(full_programs_dir, exist_ok=True)
    full_programs_file_path = os.path.join(full_programs_dir, f"{files_name}.py")
    with open(full_programs_file_path, 'w') as full_programs_file:
        full_programs_file.write(full_program)
    print(f"File created at: {full_programs_file_path}")

def get_object_from_dissasembler_and_run_code_writer_agent(file_name, object_name):
    object_description = get_file_content(disassembler_dir,file_name)
    print(object_description)
    run_code_writer_agent_for_object(object_name,object_description,file_name)


def build_all_code_and_run_full_program_agent(file_name, object_name):
    all_codes = create_string_with_all_parts_code_from_dir(object_name,file_name)
    run_full_program_agent(all_codes, file_name)



def run_agent_parameter_manipulator(prompt, file_name):
    print(f"Recived prompt to change program: {prompt}")
    start_time = datetime.now()
    print(f"Start time: {start_time.strftime(time_format)}")
    full_program = get_file_content(full_programs_dir,file_name)
    full_prompt = f"{prompt}\n\nprogram to change:\n{full_program}"
    new_program = run_parameter_manipulator_agent(full_prompt)
    print(f"Parameter manipulator agent finish runing result:\n{new_program}")
    print("------------------------------------------------------------------------------")
    print("Start creating python file with new program")

    # Save full program into file
    os.makedirs(full_programs_dir, exist_ok=True)
    formatted_prompt = prompt.replace(" ","_")
    new_file_name = f"{formatted_prompt}_{file_name}"
    full_programs_file_path = os.path.join(full_programs_dir, new_file_name)
    with open(full_programs_file_path, 'w') as full_programs_file:
        full_programs_file.write(new_program)
    print(f"File created at: {full_programs_file_path}")
    
    # Finish - time calculation
    end_time = datetime.now()
    print(f"End time: {end_time.strftime(time_format)}")
    duration = end_time-start_time
    print(f"Total runing time: {duration} in ms: {int(duration.total_seconds() * 1000)}")
    return new_program

# run_agent_parameter_manipulator("Cahnge jar height to 30 cm","A_jar_2024_02_25_12_55_34.py")
# get_object_from_dissasembler_and_run_code_writer_agent("flower_pot_1", "A round flower pot that expands upwards with protruding edges")
# build_all_code_and_run_full_program_agent("flower_pot_1", "A round flower pot that expands upwards with protruding edges")
# run_all_agents("A door handle")
# run_all_agents("S-shaped hook")
# run_all_agents("A round flower pot that expands upwards with protruding edges")
# run_all_agents("Flowerpot rack")
# run_all_agents("Toothbrush holder cup")
# run_all_agents("Dispenser for napkins in the shape of triangles that hug the napkins")
# run_all_agents("Toothpick dispenser - a round box with a lid")
run_all_agents("plate")

# run_disassembler_agent_for_prompt("A kettle with 2 handles at both sides and without a lid", "kettle_without_lid_with_2_handkes_temp15_topp01_turbo1106_23examples")






