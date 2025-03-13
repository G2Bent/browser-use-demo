#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/12
"""
import asyncio
import json
import os
from browser_use import Agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
# 查询 tracking
e2e_test = """
1. 打开页面 https://www.aftership.com/carriers
2. 点击 Try 后面的 tracking number
3. 点击 Track 按钮
4. 在新标签页检查 tracking number 是否和输入的 tracking number 一致
"""

async def main():
    # 初始化代理，指定任务和使用的语言模型
    agent = Agent(
        task=e2e_test,
        llm=ChatOpenAI(
            base_url="https://api.deepseek.com/v1",  # DeepSeek API 地址
            model="deepseek-chat",
            api_key=os.environ.get('DEEPSEEK_API_KEY')
            ),
        use_vision=False,  # 禁用视觉模式，依赖DOM解析,
        )
    # 运行代理
    result = await agent.run()
    res = json.loads(result.final_result())
    # 验证返回结果
    assert 'Tracking number not found' not in res, "查询 tracking 失败"
    print("\n======== 测试试结果 ========")