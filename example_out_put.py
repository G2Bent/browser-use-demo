#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/12
"""

from pydantic import BaseModel

import asyncio
import json
import os

from browser_use import Agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Initialize DeepSeek V3 model
llm = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",  # DeepSeek API address
        model='deepseek-chat',
        api_key=os.environ.get('DEEPSEEK_API_KEY')  # Replace with actual API key
    )

class TestCase(BaseModel):
    task: str
    llm: ChatOpenAI
    use_vision: bool = False
    sensitive_data: dict = {}

    async def run(self):
        agent = Agent(
            task=self.task,
            llm=self.llm,
            use_vision=self.use_vision,

            sensitive_data=self.sensitive_data
        )
        result = await agent.run()
        return result

async def main():
    test_case = TestCase(
        task=
        """
        1. Open https://admin.aftership.com/
        2. Enter email address x_name
        3. Enter wrong password x_password
        4. Click login button
        5. Verify page displays 'Please enter a valid email address' prompt
        """,
        llm=llm,
        sensitive_data={'x_name':'test_user', 'x_password':"wrong_pass"}
    )
    result = await test_case.run()
    res = json.loads(result.final_result())
    print("\n======== Test Result ========")
    print(res)

if __name__ == '__main__':
    asyncio.run(main())