"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional
import os
import re


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        max_turns: int = Field(
            default=8, description="Maximum allowable conversation turns for a user."
        )
        collection_name: str = Field(
            default="", description="Name of the collection for direct inclusion."
        )

    class UserValves(BaseModel):
        max_turns: int = Field(
            default=4, description="Maximum allowable conversation turns for a user."
        )
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def clean_text(self, text: str) -> str:
        # Remove multiple consecutive newlines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Replace multiple spaces with single space
        text = re.sub(r"\s+", " ", text)

        # Remove newlines between words (keep paragraph structure)
        text = re.sub(r"(\w)\n(\w)", r"\1 \2", text)

        # Trim leading and trailing whitespace
        return text.strip()

    def _get_doc_contents(self):
        from open_webui.models.knowledge import (
            Knowledges,
            KnowledgeForm,
            KnowledgeResponse,
            KnowledgeUserResponse,
        )

        from open_webui.models.files import (
            FileForm,
            FileModel,
            FileModelResponse,
            Files,
        )

        coll_name = self.valves.collection_name
        if not coll_name or len(coll_name) == 0:
            return
        kb = next(
            (kb for kb in Knowledges.get_knowledge_bases() if kb.name == coll_name),
            None,
        )
        if not kb:
            return
        doc_contents = []
        for f_id in kb.data["file_ids"]:
            f_model = Files.get_file_by_id(f_id)
            f_name = f_model.filename
            f_content = f_model.data["content"]
            doc_contents.append(f_content)
            print(f"===== {f_name}: {f_content}=====")
        return doc_contents

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        print(f"*****inlet:{__name__}")
        print(f"--- {body['metadata']['model']['params']['system']}")

        docs_contents = self._get_doc_contents()
        if docs_contents:
            print(f"\n**have doc contents: {len(docs_contents)}\n")
            content = "\n".join(docs_contents)
            cleaned_content = self.clean_text(content)

            # Prepend cleaned file content to the first message
            original_content = body["messages"][0]["content"]
            # body["messages"][0]["content"] = f"{cleaned_content}\n\n{original_content}"
            body["messages"][0]["content"] = f"{original_content}\n\n{cleaned_content}"
            print(f"***prepended: {cleaned_content}")
            # TODO: Remove files from body?
        print(f"inlet:body:*****{body}*****")
        print(f"inlet:user:*****{__user__}*****")

        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])

            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)
            if len(messages) > max_turns:
                raise Exception(
                    f"Conversation turn limit exceeded. Max turns: {max_turns}"
                )

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{__user__}")

        return body
