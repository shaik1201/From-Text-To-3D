from openai import OpenAI
from Consts.agent_code_writer_consts import *
from Consts.consts import *


def run_code_writer_agent(content):
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model=CODE_WRITER_MODEL,
        messages=[
            {
                ROLE: SYSTEM,
                CONTENT: CODE_WRITER_SYSTEM_MESSAGE
            },
            {
                ROLE: USER,
                CONTENT: content
            }
        ],
        temperature=CODE_WRITER_TEMPERATURE,
        max_tokens=CODE_WRITER_MAX_TOKENS,
        top_p=CODE_WRITER_TOP_P,
        frequency_penalty=CODE_WRITER_FREQUENCY_PENALTY,
        presence_penalty=CODE_WRITER_PRESENCE_PENALTY
    )

    result = completion.choices[0].message.content

    return result
