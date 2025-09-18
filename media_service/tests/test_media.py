import asyncio
import io
import os
import uuid

import pytest
import requests

from app.exceptions.custom_exceptions import (
    AuthorizationError,
    FileTooLargeError,
    NotFoundError,
    UnsupportedMediaTypeError,
)
from app.services.media_service import MediaService

from .utils import check_image_url, generate_db_file, generate_db_image


@pytest.mark.asyncio
async def test_upload_avatar(media_service: MediaService):
    with pytest.raises(UnsupportedMediaTypeError): # check if file type invalid
        await media_service.upload_avatar(io.BytesIO(), owner_id=uuid.uuid4(), content_type="document/png")
    with pytest.raises(UnsupportedMediaTypeError): # check if file invalid
        await media_service.upload_avatar(io.BytesIO(), owner_id=uuid.uuid4(), content_type="image/png")
    with pytest.raises(FileTooLargeError): # check if file size bigger than 5 mb
        await media_service.upload_avatar(io.BytesIO(os.urandom(6 * 1024 * 1024)), owner_id=uuid.uuid4(), content_type="image/png")

    file_db = await generate_db_image(media_service=media_service)

    check_image_url(file_db.url)

@pytest.mark.asyncio
async def test_get_file_by_id(media_service: MediaService):
    with pytest.raises(NotFoundError):
        await media_service.get_file_url(file_id=uuid.uuid4())

    file_db = await generate_db_image(media_service=media_service)

    public_url = media_service.file_service.get_public_url(f"test/{file_db.url}")
    resp = requests.get(url=public_url)
    assert resp.status_code == 403 # check if public url access denied

    url = await media_service.get_file_url(file_db.id)

    check_image_url(url) # check if image available

    await asyncio.sleep(6)

    resp = requests.get(url=url)

    assert resp.status_code == 403 # check if file url expired

    url = await media_service.get_file_url(file_db.id)

    check_image_url(url) # check if new url available

    owner_id = uuid.uuid4()

    file_db = await generate_db_file(media_service=media_service, owner_id=owner_id, visibility="private")
    
    with pytest.raises(AuthorizationError): # check if anonomly get private file
        await media_service.get_file_url(file_db.id) 
    

    with pytest.raises(AuthorizationError): # check if random user get private file
        await media_service.get_file_url(file_id=file_db.id, user_id=uuid.uuid4()) 

    file_url = await media_service.get_file_url(file_id=file_db.id, user_id=owner_id)

    check_image_url(file_url)

@pytest.mark.asyncio
async def test_delete_file(media_service: MediaService):
    with pytest.raises(NotFoundError):
        await media_service.delete_file(file_id=uuid.uuid4(), user_id=uuid.uuid4())

    file_db = await generate_db_image(media_service=media_service)

    with pytest.raises(AuthorizationError): # check if random user can delete others files
        await media_service.delete_file(file_id=file_db.id, user_id=uuid.uuid4())

    assert file_db.owner_id is not None

    await media_service.delete_file(file_id=file_db.id, user_id=file_db.owner_id)

    with pytest.raises(NotFoundError): # check if file was deleted
        await media_service.delete_file(file_id=file_db.id, user_id=uuid.uuid4())

    file_db = await generate_db_image(media_service=media_service)

    await media_service.delete_file(file_id=file_db.id, user_id=uuid.uuid4(), is_superuser=True)

