from openai import OpenAI
from Consts.agent_parameter_manipulator_consts import *
from Consts.consts import *


def run_parameter_manipulator_agent(content):
    client = OpenAI(api_key=OPENAI_API_KEY)

    completion = client.chat.completions.create(
        model=PARAMETER_MANIPULATOR_MODEL,
        messages=[
            {
                ROLE: SYSTEM,
                CONTENT: PARAMETER_MANIPULATOR_SYSTEM_MESSAGE
            },
            {
                ROLE: USER,
                CONTENT: content
            }
        ],
        temperature=PARAMETER_MANIPULATOR_TEMPERATURE,
        max_tokens=PARAMETER_MANIPULATOR_MAX_TOKENS,
        top_p=PARAMETER_MANIPULATOR_TOP_P,
        frequency_penalty=PARAMETER_MANIPULATOR_FREQUENCY_PENALTY,
        presence_penalty=PARAMETER_MANIPULATOR_PRESENCE_PENALTY
    )

    result = completion.choices[0].message.content

    return result