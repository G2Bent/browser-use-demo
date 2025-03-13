#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/8
"""
# browser/browser.py
from playwright.async_api import async_playwright

class BrowserManager:
    def __init__(self, config):
        self.config = config  # 来自settings.py的配置

    async def launch(self):
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(
            headless=self.config.HEADLESS,
            args=self.config.BROWSER_ARGS
        )
        return browser