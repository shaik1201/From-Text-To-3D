DISASSEMBLER_MODEL = "ft:gpt-3.5-turbo-0125:personal:disassembler-35:96i2syeN"
DISASSEMBLER_SYSTEM_MESSAGE = "You will provided with object name.\nDefine a list of object parts.\nInclude only the 3D shape that consist the object and not its electronic parts.\nFor every part :\n- Describe the part shape as an independent 3d object\n- List part parameters\n- Define part orientation by\n -- origin point\n -- normal vector\n- Define part alignment when the part is not 360 degree symmetric around its normal"
DISASSEMBLER_TEMPERATURE = 1.85
DISASSEMBLER_MAX_TOKENS = 2048
DISASSEMBLER_TOP_P = 0.3
DISASSEMBLER_FREQUENCY_PENALTY = 0
DISASSEMBLER_PRESENCE_PENALTY = 0
