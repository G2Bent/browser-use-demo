#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/12
"""
import os

from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio

# 初始化DeepSeek V3模型
llm = ChatOpenAI(
        model='deepseek-chat',
        base_url="https://api.deepseek.com/v1",
        # model='qwq-32b',
        api_key=os.environ.get('DEEPSEEK_API_KEY')  # 替换为实际API密钥
    )

initial_actions = [
	{'open_tab': {'url': 'https://www.google.com'}},
	{'open_tab': {'url': 'https://en.wikipedia.org/wiki/Randomness'}},
	{'scroll_down': {'amount': 1000}},
]

async def main():
    agent = Agent(
        task="""
        1. 查找北京到上海的火车票
        """,
        llm=llm,
        save_conversation_path="logs/conversation",  # Save chat logs
        use_vision=False,  # 禁用视觉模式，依赖DOM解析,
        )
    result = await agent.run(max_steps = 3)
    print(result)
    print(result.urls())
    print(result.final_result())

    agent.stop()
asyncio.run(main())