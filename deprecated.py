from openai import OpenAI, AsyncOpenAI
from openai.types.beta.threads.message import Message
from openai.pagination import SyncCursorPage
from typing import Optional, List

import asyncio

from time import time

from example import dialogue
from secrets import openai_api_key


# system_msg = """
# 대화 내역의 사람들은 "피임약은 권장되어야 한다"를 주제로 채팅방에서 토론을 하고 있어. 
# 주어진 이전 채팅 기록을 바탕으로 target 메세지가 주장인지, 특정 주장에 동의하는 말인지, 둘 다 아닌지 분류해.

# 주장은 1, 특정 주장에 동의하는 말 2, 둘다 아니면 0으로 분류해.
# e.g.
# 1
# """
system_msg = """
대화 내역의 사람들은 "피임약은 권장되어야 한다"를 주제로 채팅방에서 토론을 하고 있어. 
target 메세지가 주장인지, 특정 주장에 동의하는 말인지, 둘 다 아닌지 분류해.

주장은 1, 특정 주장에 동의하는 말 2, 둘다 아니면 0으로 분류해.
e.g.
1
"""

# target = "Target:\n영지버섯: 피임약도 제대로 먹으면 효과 좋은뎅..ㅋㅋ"

# msgs = [
#     {"role": "system", "content": system_msg},
#     {"role": "user", "content": target},
#     {"role": "user", "content": f"""
#       [대화내역]
#      {"\n".join(dialogue)}
# """}
# ]


# def create_msg(chat_end: int):
    
#     part = dialogue[:chat_end]
#     # print(part[-1])

#     return [
#         {"role": "system", "content": system_msg},
#         {"role": "user", "content": f"Target: {part[-1]}"},
#         {"role": "user", "content": f"""
#        [대화내역]
#      {"\n".join(part)}
#      """}
#     ]

def create_msg2(target: str):
    

    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": f"Target: {target}"},
    ]






client = AsyncOpenAI(api_key=openai_api_key)
async def run_devill(messages):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    choices = response.choices

    if len(choices) > 0:
        return choices[0].message.content
    else:
        return None


# async def test(chatend: int):
#     tmp = time()
#     answer = await run_devill(create_msg(chat_end=chatend))
#     tmp2 = time()
#     elapsed = round(tmp2 - tmp, 3)


#     print(f"{answer}, {elapsed}, {dialogue[chatend - 1]}")

# 2- len
# for i in range(1, len(dialogue)):
#   asyncio.run(test(i))

async def test2(target_index):
    _target = dialogue[target_index]
    tmp = time()
    answer = await run_devill(create_msg2(target=_target))
    tmp2 = time()
    elapsed = round(tmp2 - tmp, 3)

    print(f"{answer}, {elapsed}, {_target}")
  
for i in range(0, len(dialogue)):
  asyncio.run(test2(i))