"""Helper for uploading files to the memory store."""

import asyncio
import os
from typing import Any

import httpx


MEMORY_UPLOAD_URL = "http://localhost:9001/upload"
MEMORY_STATUS_URL = "http://localhost:9001/upload-status"


async def upload_files(
    document_id: str,
    files: list[str],
    index: str = "default",
    steps: list[str] | None = None,
    tags: list[str] | None = None,
) -> None:
    """Upload one or more files under a given document_id and tags."""

    steps = steps or None

    # build form fields
    data: dict[str, str | list[str]] = {
        "index": index,
        "documentId": document_id,
    }

    # httpx will encode lists as repeated fields
    if tags:
        data["tags"] = tags

    if steps:
        data["steps"] = steps

    # prepare file tuples: (field_name, (filename, fileobj, content-type))
    files_payload: list[tuple[str, tuple[str, object, str]]] = []

    for path in files:
        filename = os.path.basename(path)
        f = open(path, "rb")
        files_payload.append(("files", (filename, f, "application/octet-stream")))

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url=MEMORY_UPLOAD_URL,
            data=data,
            files=files_payload,
        )
        print(resp)
        resp.raise_for_status()

    # check the status periodically
    all_completed = False
    while not all_completed:
        await asyncio.sleep(4)  # sleep for a bit.
        try:
            status = await get_upload_status(document_id=document_id, index=index)

            all_completed = status.get("completed", False)
        except Exception:
            # ignore an continue
            continue

    print("FILE UPLOAD COMPLETE.")

    # close all file handles
    for _, (_fn, fh, _ct) in files_payload:
        fh.close()


async def get_upload_status(
    document_id: str,
    index: str = "default",
) -> dict[str, Any]:
    """Check processing status for a previously uploaded document."""

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url=MEMORY_STATUS_URL,
            params={
                "documentId": document_id,
                "index": index,
            },
        )

        resp.raise_for_status()
        return resp.json()
