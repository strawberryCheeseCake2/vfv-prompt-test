from openai import OpenAI, AsyncOpenAI
from openai.types.beta.threads.message import Message
from openai.pagination import SyncCursorPage
from typing import Optional, List

import asyncio

from time import time
from datetime import datetime

# from example import dialogue2
from pilot_processing import messages, Message

from secret import openai_api_key


clf_sys_msg = """
[대화 내역]의 사람들은 어떤 직원을 승진시켜야 할지 채팅방에서 토론을 하고 있어. 
[Target] 메세지가 특정 직원을 승진시켜야 한다는 주장인지 아닌지 분류해.

특정 직원을 승진시켜야 한다는 주장은 1, 아니면 0으로 분류해.
e.g.
1
"""




def create_critique_msg(part: List, last_chat: str):
    br = "\n"
    return [
        {"role": "system", "content": clf_sys_msg},
        {"role": "system", "content": f"[Target]: {last_chat}\n"},
        {"role": "user", "content": f"""
         대화자수: 4\n
        [대화내역]\n
     {br.join(part)}
"""}
    ]



client = AsyncOpenAI(api_key=openai_api_key)
async def run_gpt(model: str, messages, temp: float):
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temp,
    )

    choices = response.choices

    if len(choices) > 0:
        return choices[0].message.content
    else:
        return None


async def test(chatend: int, elapsed):
    clf_init_time = time()
    last_message = messages[chatend]

    if last_message.elapsed_time > elapsed:
      await asyncio.sleep((msg.elapsed_time - elapsed).seconds)

    part = map(lambda x: x.message, messages[:chatend + 1])

    msgs = create_critique_msg(part=part, last_chat=last_message.message)
    print(msgs)
    answer = await run_gpt(model="gpt-4o", messages=msgs, temp=0.0)
    clf_completion_time = time() - clf_init_time
    elapsed = round(clf_completion_time, 3)

    print(f"{answer}, {elapsed}, {messages[chatend]}")


start = datetime.now()

for i in range(0, len(messages)):
  msg = messages[i]
  if msg.message.startswith("DEVIL:"):
    continue
  
  elapsed = datetime.now() - start

  asyncio.run(test(i, elapsed))

