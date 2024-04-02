from openai import OpenAI
from Consts.agent_assembler_consts import *
from Consts.consts import *
from Utils.file_utils import *
from Utils.model_utils import *

def run_assembler_agent(content):
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model=ASSEMBLER_MODEL,
        messages=[
            {
                ROLE: SYSTEM,
                CONTENT: ASSEMBLER_SYSTEM_MESSAGE
            },
            # {
            #     ROLE: USER,
            #     CONTENT: create_string_with_all_parts_code_from_dir("A bowl","bowl_1")
            # },
            # {
            #     ROLE: ASSISTANT,
            #     CONTENT: get_file_content(full_program_files_dir,"bowl_1.py")
            # },
            # {
            #     ROLE: USER,
            #     CONTENT: create_string_with_all_parts_code_from_dir("A mug","mug_1")
            # },
            # {
            #     ROLE: ASSISTANT,
            #     CONTENT: get_file_content(full_program_files_dir,"mug_1.py")
            # },
            # {
            #     ROLE: USER,
            #     CONTENT: create_string_with_all_parts_code_from_dir("A cooking pot","cooking_pot_1")
            # },
            # {
            #     ROLE: ASSISTANT,
            #     CONTENT: get_file_content(full_program_files_dir,"cooking_pot_1.py")
            # },
            {
                ROLE: USER,
                CONTENT: content
            }
        ],
        temperature=ASSEMBLER_TEMPERATURE,
        max_tokens=ASSEMBLER_MAX_TOKENS,
        top_p=ASSEMBLER_TOP_P,
        frequency_penalty=ASSEMBLER_FREQUENCY_PENALTY,
        presence_penalty=ASSEMBLER_PRESENCE_PENALTY
    )

    result = completion.choices[0].message.content

    return result
