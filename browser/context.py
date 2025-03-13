#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author : bw.ling
create_time : 2025/3/8
"""
# browser/context.py
class ContextManager:
    @staticmethod
    async def create_context(browser, config):
        context = await browser.new_context(
            viewport=config.VIEWPORT_SIZE,
            locale=config.LOCALE,
            user_agent=config.USER_AGENT
        )
        if config.COOKIES_FILE:
            await context.add_cookies(load_cookies(config.COOKIES_FILE))
        return context