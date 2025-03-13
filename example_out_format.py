#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/12
"""
import asyncio
import os
from typing import List

from browser_use import Agent
from browser_use.controller.service import Controller
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()


# Define the output format as a Pydantic model
class Post(BaseModel):
    tracking_number: str


class Posts(BaseModel):
    posts: List[Post]


controller = Controller(output_model=Posts)

e2e_test = """
1. 打开页面 https://www.aftership.com/carriers
2. 点击 Try 后面的 tracking number
3. 点击 Track 按钮
4. 在新标签页检查 tracking number 是否和输入的 tracking number 一致
"""

# 初始化DeepSeek V3模型
llm = ChatOpenAI(
    base_url="https://api.deepseek.com/v1",  # DeepSeek API 地址
    model='deepseek-chat',

    api_key=os.environ.get('DEEPSEEK_API_KEY')  # 替换为实际API密钥
    )


async def main():
    task = e2e_test
    model = llm
    # use_vision = False,  # 禁用视觉模式，依赖DOM解析
    agent = Agent(task=task, llm=model, use_vision=False, controller=controller)

    history = await agent.run()

    result = history.final_result()
    if result:
        parsed: Posts = Posts.model_validate_json(result)

        for post in parsed.posts:
            print('\n--------------------------------')
            print(f'tracking_number:              {post.tracking_number}')
    else:
        print('No result')


if __name__=='__main__':
    asyncio.run(main())
