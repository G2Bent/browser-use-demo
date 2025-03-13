#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/12
"""
import os

from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContextConfig, BrowserContext
from langchain_openai import ChatOpenAI

"""
Test dropdown interaction functionality.
"""
import pytest
from browser_use.agent.service import Agent
from browser_use.agent.views import AgentHistoryList

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
context = BrowserContext(browser=Browser()
, config=config)

llm = ChatOpenAI(
        base_url='https://api.deepseek.com/v1',
        model='deepseek-chat',
        # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        # model='qwq-32b',
        api_key=os.environ.get('DEEPSEEK_API_KEY')  # 替换为实际API密钥
    )

@pytest.mark.asyncio
async def test_dropdown():
    """Test selecting an option from a dropdown menu."""
    agent = Agent(
        task=(
            'go to https://codepen.io/geheimschriftstift/pen/mPLvQz and first get all options for the dropdown and then select the 5th option'
        ),
        llm=llm,
        browser_context=context,
        )

    try:
        history: AgentHistoryList = await agent.run(20)
        result = history.final_result()

        # Verify dropdown interaction
        assert result is not None
        assert 'Duck' in result, "Expected 5th option 'Duck' to be selected"

        # Verify dropdown state
        element = await context.get_element_by_selector('select')
        assert element is not None, "Dropdown element should exist"

        value = await element.evaluate('el => el.value')
        assert value=='5', "Dropdown should have 5th option selected"

    except Exception as e:
        pytest.fail(f"Dropdown test failed: {str(e)}")
    finally:
        await context.close()
