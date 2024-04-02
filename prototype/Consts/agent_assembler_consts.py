ASSEMBLER_MODEL = "ft:gpt-3.5-turbo-0125:personal:web-assem:99V1eAJZ" # "gpt-3.5-turbo-16k"
ASSEMBLER_SYSTEM_MESSAGE = "Your role is to create full program out of several parts."
# ASSEMBLER_SYSTEM_MESSAGE = "Your role is to create full program out of several parts.\nThe united output should be in as array parameter a.\nStructure of full program:\n- All imports\n- Constant parameters\n- All functions of the different parts include implementation\n- List of parameters from all the parts\n- calling every function of each part\n- and eventually all the part in array named 'a':\na = [part1, part2, ....]"
ASSEMBLER_TEMPERATURE = 0.05
ASSEMBLER_MAX_TOKENS = 4096
ASSEMBLER_TOP_P = 0.05
ASSEMBLER_FREQUENCY_PENALTY = 0
ASSEMBLER_PRESENCE_PENALTY = 0