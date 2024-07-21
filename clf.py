from openai import OpenAI, AsyncOpenAI
from openai.types.beta.threads.message import Message
from openai.pagination import SyncCursorPage
from typing import Optional, List

import asyncio

from time import time

from example import dialogue
from secrets import openai_api_key


critique_sys_msg = """
대화 내역의 사람들은 "피임약은 권장되어야 한다"를 주제로 채팅방에서 토론을 하고 있어. 
주어진 이전 채팅 기록을 바탕으로 target 메세지가 주장인지, 특정 주장에 동의하는 말인지, 둘 다 아닌지 분류해.

주장은 1, 특정 주장에 동의하는 말 2, 둘다 아니면 0으로 분류해.
e.g.
1
"""


def create_critique_msg(part: List):

    return [
        {"role": "system", "content": critique_sys_msg},
        {"role": "user", "content": f"""
         대화자수: 4\n
        [대화내역]\n
     {"\n".join(part)}
"""}
    ]



client = AsyncOpenAI(api_key=openai_api_key)
async def run_gpt(model: str, messages, temp: float):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp
    )

    choices = response.choices

    if len(choices) > 0:
        return choices[0].message.content
    else:
        return None


async def test(chatend: int):
    cr_init_time = time()

    part = dialogue[:chatend + 1]

    msgs = create_critique_msg(part=part)
    answer = await run_gpt(model="gpt-4o", messages=msgs, temp=0.0)
    cr_completion_time = time() - cr_init_time
    elapsed = round(cr_completion_time, 3)

    print(f"{answer}, {elapsed}, {dialogue[chatend]}")


for i in range(0, len(dialogue)):
  asyncio.run(test(i))

