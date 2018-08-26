from unittest import TestCase

import asyncio
from asynctest import Mock


class AsyncTest(TestCase):
    def mock_coroutine(self, *args, **kwargs):
        m = Mock(*args, **kwargs)

        async def mock_coroutine(*args, **kwargs):
            return m(*args, **kwargs)

        mock_coroutine.mock = m
        return mock_coroutine

    def run_coroutine(self, coroutine):
        return asyncio.get_event_loop().run_until_complete(coroutine)
