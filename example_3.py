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
# 测试登录失败场景
test_case = """
1. 打开 https://admin.aftership.com/
2. 输入用户名'test_user'
3. 输入错误密码'wrong_pass'
4. 点击登录按钮
5. 验证页面显示'Please enter a valid email address'提示
"""
# 查询 tracking
e2e_test = """
1. 打开页面 https://www.aftership.com/carriers
2. 点击 Try 后面的 tracking number
3. 点击 Track 按钮
4. 在新标签页检查 tracking number 是否和输入的 tracking number 一致
"""

# 登录 admin
admin_test = """
1. 打开 https://admin.aftership.com/
2. 输入用户名 x_name
3. 输入正确密码 x_password
4. 点击登录按钮
5. 验证页面跳转到 admin 首页
"""


async def main():
    # 初始化代理，指定任务和使用的语言模型
    agent = Agent(
        task=test_case,
        llm=ChatOpenAI(
            base_url="https://api.deepseek.com/v1",  # DeepSeek API 地址
            model="deepseek-chat",
            api_key=os.environ.get('DEEPSEEK_API_KEY')
            ),
        use_vision=False,  # 禁用视觉模式，依赖DOM解析,
        # sensitive_data={'x_name':'bw.ling+deletion01@aftership.com', 'x_password':'@Aftership01@'}
        )
    # 运行代理
    result = await agent.run()
    res = json.loads(result.final_result())
    # 验证返回结果
    # assert 'Please enter a valid email address' in res, "登录失败提示错误"
    print("\n======== 测试结果 ========")
# 执行异步任务
asyncio.run(main())
