#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/12
"""
import os
import pytest
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent

load_dotenv()

# 初始化DeepSeek V3模型
llm = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",  # DeepSeek API 地址
        model='deepseek-chat',
        api_key=os.environ.get('DEEPSEEK_API_KEY')  # 替换为实际API密钥
    )

# 定义 UI ��试任务
test_case = [
    {
        "task": """
        1. 打开 https://admin.aftership.com/
        2. 输入用户名'test_user'
        3. 输入错误密码'wrong_pass'
        4. 点击登录按钮
        5. 验证页面显示'Please enter a valid email address'提示
        """,
        "sensitive_data": {'x_name':'test_user', 'x_password':"wrong_pass"}
    },
    {
        "task": """
        1. 打开页面 https://www.aftership.com/carriers
        2. 点击 Try 后面的 tracking number
        3. 点击 Track 按钮
        4. 在新标签页检查 tracking number 是否和输入的 tracking number 一致
        """
    },
    {
        "task": """
        1. 打开 https://admin.aftership.com/
        2. 输入用户名 x_name
        3. 输入正确密码 x_password
        4. 点击登录按钮
        5. 验证页面跳转到 admin 首页
        """
    }
    ]

# 定义 E2E ��试任务
e2e_test = """
1. 打开页面 https://www.aftership.com/carriers
2. 点击 Try 后面的 tracking number
3. 点击 Track 按钮
4. 在新标签页检查 tracking number 是否和输入的 tracking number 一致
"""

@pytest.mark.asyncio
async def test_ui_and_e2e_tasks():
    # 创建代理并执行 UI 任务
    for case in test_case:
        agent = Agent(
            task=case["task"],
            llm=llm,
            sensitive_data=case["sensitive_data"]
        )
        result = await agent.run()
        assert "Please enter a valid email address" not in result.final_result(), f"Task {case['task']} failed"
        print(f"Task {case['task']} passed")
        # 执行 E2E 任务
        agent = Agent(
            task=e2e_test,
            llm=llm
        )
        result = await agent.run()
        assert "Tracking number is correct" in result.final_result(), f"Task {e2e_test} failed"
        print(f"Task {e2e_test} passed")
        print("============================")

if __name__ == '__main__':
    pytest.main(['-v', __file__])