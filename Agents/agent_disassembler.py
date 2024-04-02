from openai import OpenAI
from Consts.agent_disassembler_consts import *
from Consts.consts import *


def run_disassembler_agent(content):
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model=DISASSEMBLER_MODEL,
        messages=[
            {
                ROLE: SYSTEM,
                CONTENT: DISASSEMBLER_SYSTEM_MESSAGE
            },
            {
                ROLE: USER,
                CONTENT: content
            }
        ],
        temperature=DISASSEMBLER_TEMPERATURE,
        max_tokens=DISASSEMBLER_MAX_TOKENS,
        top_p=DISASSEMBLER_TOP_P,
        frequency_penalty=DISASSEMBLER_FREQUENCY_PENALTY,
        presence_penalty=DISASSEMBLER_PRESENCE_PENALTY
    )

    result = completion.choices[0].message.content

    return result
