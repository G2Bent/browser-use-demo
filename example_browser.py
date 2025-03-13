#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/12
"""
import os

from browser_use.browser.context import BrowserContext
from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use import Browser, BrowserConfig, BrowserContextConfig

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

config = BrowserContextConfig(
    # cookies_file="path/to/cookies.json",
    # wait_for_network_idle_page_load_time=3.0,
    # browser_window_size={'width': 1280, 'height': 1100},
    locale='en-US',
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    highlight_elements=True,
    # viewport_expansion=500,
    # allowed_domains=['google.com', 'wikipedia.org'],
)
context = BrowserContext(browser=Browser(
    config=BrowserConfig(
        # chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        )
    )
, config=config)

llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-chat',
        api_key=os.environ.get('DEEPSEEK_API_KEY')  # ��换为实际API密钥
    )
# 查询 tracking
e2e_test = """
1. 打开页面 https://www.aftership.com/carriers
2. 点击 Try 后面的 tracking number
3. 点击 Track 按钮
4. 在新标签页检查 tracking number 是否和输入的 tracking number 一致
"""

agent = Agent(
        browser_context=context,
        task=e2e_test,
        llm=llm,
        )
result = agent.run()
print(result)