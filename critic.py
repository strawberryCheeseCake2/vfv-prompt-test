from openai import OpenAI, AsyncOpenAI
from openai.types.beta.threads.message import Message
from openai.pagination import SyncCursorPage
from typing import Optional, List

import asyncio

from time import time

from example import dialogue
from secrets import openai_api_key

critique_sys_msg = """
대화 내역의 사람들은 "피임약은 권장되어야 한다"를 주제로 토론을 하고 있어. 
너는 악마의 대변인이야. 
대화 내역을 바탕으로 찬성측의 말에서 다시 생각해봐야 할 점을 상기시켜줘
말할 때는 처음에 공감을 해준 후에 "~도 생각해보면 어떨까요?"식으로 부드럽게  2-3 문장이내로 말해

이미 언급한 비판을 반복하지말고 똑같은 표현을 반복하지마. 대화 내역에서 언급된 내용도 반복하지마. 두번이상 반복된 근거에 비판할 떄는 다른 건 아무것도 입력하지말고 ...만 입력해
"""

clf_sys_msg = """
대화 내역의 사람들은 "피임약은 권장되어야 한다"를 주제로 채팅방에서 토론을 하고 있어. 
target 메세지가 주장인지, 특정 주장에 동의하는 말인지, 둘 다 아닌지 분류해.

주장은 1, 특정 주장에 동의하는 말 2, 둘다 아니면 0으로 분류해.
e.g.
1
"""

invoke_indices = [14, 21, 31]
selected = invoke_indices[0]

client = AsyncOpenAI(api_key=openai_api_key)


def create_critique_msg(part: List):

    return [
        {"role": "system", "content": critique_sys_msg},
        {"role": "user", "content": f"""
         대화자수: 4
        [대화내역]\n
     {"\n".join(part)}
"""}
    ]

def create_clf_msg(part: List, last_chat):
    
    print(f"Last Chat: {last_chat}")
    print()
    return [
        {"role": "system", "content": clf_sys_msg},
        {"role": "user", "content": f"target: {last_chat}"},
        {"role": "user", "content": f"""
        [대화내역]\n
     {"\n".join(part)}
"""}
    ]

async def get_critique_stream(messages):
    stream = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )

    return stream
    

async def test(target_index):
    
    part = dialogue[:target_index + 1]
    last_chat = part[-1]
    # print(last_chat)


    cl_init_time = time()

    clf_res = await client.chat.completions.create(
        model="gpt-4o",
        messages=create_clf_msg(part=part, last_chat=last_chat)
    )
    clf = clf_res.choices[0].message.content
    cl_elapsed_time = time() - cl_init_time
    print(f"clf_result: {clf}")
    print(f"cl_elapsed_time: {cl_elapsed_time}")
    print()
    cr_init_time = time()
    critique_msg = create_critique_msg(part=part)
    critique_stream = await get_critique_stream(messages=critique_msg)

    isFirstChunk = True
    completion_buffer = ""
    time_to_first_token = 0.0


    async for chunk in critique_stream:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            
            completion_buffer += chunk_content

            if isFirstChunk:
                isFirstChunk = False
                time_to_first_token = time() - cr_init_time

    print(f"Time to First Token: {time_to_first_token}")
    print(f"Critique Result: {completion_buffer}")
    print()    



async def loop_test():
    for idx in invoke_indices:
        await test(idx)


asyncio.run(loop_test())