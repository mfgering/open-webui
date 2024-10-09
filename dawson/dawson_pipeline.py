"""
title: Dawson Pipeline
author: mike-gering
author_url: https://github.com/justinh-rahb/webui-doom
funding_url: https://github.com/justinh-rahb/webui-doom
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Union, Generator, Iterator, Dict
from utils.misc import get_last_user_message
from apps.webui.models.files import Files
from apps.webui.models.users import Users

import requests
import time
import uuid
import os
import json
from typing import Callable, AsyncGenerator, Awaitable, Optional, Protocol


class Pipe:
    class Valves(BaseModel):
        ROUTER_ID: str = Field(
            default="semantic-router",
            description="Identifier for the semantic router model.",
        )
        ROUTER_NAME: str = Field(
            default="Semantic Router", description="Name for the semantic router model."
        )
        OPENAI_BASE_URL: str = Field(
            default="http://host.docker.internal:11434/v1",
            description="OpenAI Compatible URL for local models",
        )

    def __init__(self):
        self.type = "pipe"
        self.valves = self.Valves()

    def setup(self):
        v = self.valves
        if not v.OPENAI_API_KEY or not v.OPENAI_BASE_URL:
            raise Exception("Error: OPENAI_API_KEY or OPENAI_BASE_URL is not set")
        self.openai_kwargs = {
            "base_url": v.OPENAI_BASE_URL,
            "api_key": v.OPENAI_API_KEY,
        }
        lf = (v.LANGFUSE_SECRET_KEY, v.LANGFUSE_PUBLIC_KEY, v.LANGFUSE_URL)
        if not all(lf):
            self.langfuse_kwargs = None
        else:
            self.langfuse_kwargs = {
                "secret_key": v.LANGFUSE_SECRET_KEY,
                "public_key": v.LANGFUSE_PUBLIC_KEY,
                "host": v.LANGFUSE_URL,
            }

    async def pipe(
        self,
        body: dict,
        __user__: dict | None,
        __task__: str | None,
        __tools__: dict[str, dict] | None,
    ) -> AsyncGenerator:
        print(__task__)
        print(f"{__tools__=}")
        if __task__ == "function_calling":
            return

        self.setup()
        print(f"******** end of pipe()")
