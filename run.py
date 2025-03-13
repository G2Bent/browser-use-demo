#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/8
"""
import json

from browser_use import Browser
from browser_use.browser.browser import BrowserConfig
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio, os
from dotenv import load_dotenv
from browser_use.browser.context import BrowserContextConfig, BrowserContext

# 加载环境变量
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

async def main():
    # 初始化DeepSeek V3模型
    llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-chat',
        # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        # model='qwq-32b',
        api_key=os.environ.get('DEEPSEEK_API_KEY')  # 替换为实际API密钥
    )
    # llm = ChatOllama(
    #     # model='qwen2.5:32b-instruct-q4_K_M',
    #     # model='qwen2.5:14b',
    #     model='qwen2.5:latest',
    #     num_ctx=128000,
    #     ),
    # 创建Agent并定义UI测试任务
    agent = Agent(
        # browser_context=context,
        task=
        """
        1. 访问 BTP 首页（https://aftership2021.aftership.com/）
        2. 在 Tracking number 输入框中输入 "ITD-0-12345678",
        3. 点击 "Track" 按钮
        4. 点击 "Show all"
        5. 提取弹窗页面的所有信息
        用 json 格式返回，包含以下字段：
        - tracking_number
        - status
        - carrier
        - checkpoints
        """,
        llm=llm,
        use_vision=False,  # 禁用视觉模式，依赖DOM解析
        max_failures = 3,  # 失败时自动重试次数
        retry_delay = 10,  # 重试间隔时间
    )
    # 执行任务后输出结果
    result = await agent.run()
    # json解析
    res = json.loads(result.final_result())
    # assert len(res)==10, f"实际获取新闻数量不足，预期10条，实际{len(result.final_result())}条"
    #
    # for news_item in res:  # 检查前十条
    #     assert 'title' in news_item, "新闻条目缺少标题字段"
    #     assert 'publish_time' in news_item, "新闻条目缺少发布时间字段"
    #     assert news_item['title'].strip(), "新闻标题内容为空"
    #     assert news_item['publish_time'].strip(), "发布时间内容为空"
    print("\n======== 测试结果 ========")
    print(result.final_result())
    await context.close()

if __name__ == '__main__':
    asyncio.run(main())