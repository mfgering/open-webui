"""
title: Full Document Filter (2)
author: Mike
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

"""
What it does:
  - This filter prepends the full document contents of a given collection
    to the first message of a chat.
How to install:
  1. Add the function definition to OWUI (+ on Admin Panel/Functions page)
  2. Enable the function (Admin Panel/Functions)
  3. Edit the valves for the function (settings on Admin Panel/Functions page)
     Enter the name of a document collection
  4. Create/edit a workspace model (Workspace/Models)
  5. Check the box to enable this filter for the model
  6. Save/Update the model config

How to use:
  1. Create a document collection, e.g. foo
  2. Configure the collection name valve to this filter to refer to it, .e.g. "foo"
  3. You probably do not want to add this collection to the model's knowledge.

Notes:
  - Set or update the model's system prompt to introduce this content
  
"""
from pydantic import BaseModel, Field
from typing import Optional
import os
import re
from open_webui.models.knowledge import Knowledges
from open_webui.models.files import Files


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        collection_name: str = Field(
            default="", description="Name of the collection for direct inclusion."
        )

    def __init__(self):
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
            # print(f"===== {f_name}: {f_content}=====")
        return doc_contents

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # print(f"*****inlet:{__name__}")
        docs_contents = self._get_doc_contents()
        if docs_contents:
            # print(f"\n**have doc contents: {len(docs_contents)}\n")
            content = "\n".join(docs_contents)
            cleaned_content = self.clean_text(content)

            # Prepend cleaned file content to the first message
            original_content = body["messages"][0]["content"]
            body["messages"][0]["content"] = f"{cleaned_content}\n\n{original_content}"
        #print(f"inlet:body:*****{body}*****")
        # print(f"inlet:user:*****{__user__}*****")
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # print(f"outlet:{__name__}")
        # print(f"outlet:body:{body}")
        # print(f"outlet:user:{__user__}")
        return body
