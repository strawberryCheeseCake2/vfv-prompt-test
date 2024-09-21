from openai import OpenAI, AsyncOpenAI
from openai.types.beta.threads.message import Message
from openai.pagination import SyncCursorPage
from typing import Optional, List

import asyncio

from time import time

# from example import dialogue
from pilot_processing import chat_history
from secret import openai_api_key


cr_sys_msg = """
대화 내역의 사람들은 [직원 리스트]의 직원 중 어떤 직원을 승진시켜야 할지 채팅방에서 토론을 하고 있어. 
너는 Socratic Questioning을 통해 사람들이 다시 생각해보아야 할 점을 상기시켜 주는 악마의 대변인이야.
[Target]에 해당하는 입장에서 다시 생각해봐야 할 점을 알려줘.

말할 때는 처음에 공감을 해준 후에 "~도 생각해보면 어떨까요?"식으로 부드럽게  2-3 문장이내로 말해
이미 언급한 비판을 반복하지말고 똑같은 표현을 반복하지마. 대화 내역에서 언급된 내용도 반복하지마.

[Target]
토론 참가자 4명 중 2명 이상이 지지하는 입장
"""

emp_info = """
[직원 리스트]
프로필 1
(부서:영업 및 마케팅
학력: 석사 이상
올해 이수한 교육 횟수: 1회 (평균 점수: 49/100)
나이: 35세
성별: 여성
전년도 성과 평가: 5점 만점에 5점
근무 기간: 8년
수상 경력: 없음),
프로필 2(
부서: 운영
학력: 학사
올해 이수한 교육 횟수: 1회 (평균 점수: 60/100)
나이: 30세
성별: 남성
전년도 평가: 5점 만점에 3점
근무 기간: 7년
수상 경력: 없음),
프로필 3(
부서: 기술
학력: 학사
올해 이수한 교육 횟수: 1회 (평균 점수: 73/100)
나이: 45세
성별: 남성
전년도 평가: 5점 만점에 3점
근무 기간: 2년
수상 경력: 없음),
프로필 4(
부서: 분석
학력: 학사
올해 이수한 교육 횟수: 2회 (평균 점수: 85/100)
나이: 31세
성별: 남성
전년도 평가: 5점 만점에 3점
근무 기간: 7년
수상 경력: 없음),
프로필 5(
부서: 연구 및 개발
학력: 석사 이상
올해 이수한 교육 횟수: 1회 (평균 점수: 84/100)
나이: 37세
성별: 남성
전년도 성과 평가: 5점 만점에 3점
근무 기간: 7년
수상 경력: 없음)
"""

client = AsyncOpenAI(api_key=openai_api_key)


def create_critique_msg(part: List):
    br = "\n"
    return [
        {"role": "system", "content": cr_sys_msg},
        {"role": "user", "content": emp_info},
        {"role": "user", "content": f"""
        [대화내역]\n
     {br.join(part)}
      """},
      {"role": "user", "content": "2-3문장으로 짧게 답해"}
    ]


async def get_critique(messages, stream: bool = False):
    res = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=stream,
            max_tokens=256,
            temperature=1.1
        )

    return res
    
async def request_response(last_index):
    
    part = map(lambda x: x.message, chat_history[:last_index + 1])
    _start_time = time()

    openai_messages = create_critique_msg(part=part)
    result = await get_critique(messages=openai_messages)

    print(f"Index: {last_index}")
    print(f"Elapsed: {time() - _start_time}")
    print(f"Critique Result: {result.choices[0].message.content}")
    return


async def test():
    for idx, history in enumerate(chat_history):
        if history.message.startswith("DEVIL:"):
          await request_response(last_index=idx - 1)


asyncio.run(test())