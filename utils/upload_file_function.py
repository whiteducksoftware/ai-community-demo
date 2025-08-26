"""Helper for uploading files to the memory store."""

import json
import uuid

import httpx

from settings import APP_SETTINGS

async def delete_files(file_ids: list[str]) -> None:
    """Remove the uploaded files after the demo"""
    
    api_key = APP_SETTINGS.azure_api_key
    
        
    url = APP_SETTINGS.memory_upload_url.replace("/embed", "/documents")
    
    async with httpx.AsyncClient() as client:
        response = await client.request(
            url=url,
            headers={
                'api-key': api_key
            },
            json={
                'ids': file_ids,
            },
            method="DELETE"
        )
        
        print(response.content)
        
        
        
        
        


async def upload_files(
    files: list[str],
) -> list[str]:
    """Upload one or more files under a given document_id and tags."""
    
    api_key = APP_SETTINGS.azure_api_key
    
    file_ids: list[str] = []
    
    # foreach file upload it
    for file in files:
        print(f'Uploading file: {file}')
        url = APP_SETTINGS.memory_upload_url
        file_id = str(uuid.uuid4())
        data = {
            'file_id': file_id,
        }
        
        async with httpx.AsyncClient() as client:
            with open(file, 'rb') as f:
                file_to_upload = {
                    'file': (file, f)
                }
                
                response = await client.post(
                    url=url,
                    files=file_to_upload,
                    data=data,
                    headers={
                        'api-key': api_key,
                    }
                )
                
                if response.status_code == 200:
                    print(f'SUCCESS: file: {file}')
                    file_id = json.loads(response.content).get("file_id")
                    file_ids.append(file_id)
                else:
                    print(f'ERROR: file: {file}')
                    print(f'{response.status_code}:\n{str(response.content)}')
        
    return file_ids
            

