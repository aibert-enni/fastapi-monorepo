import io
import uuid
from typing import Literal
from urllib.parse import urlparse

import requests
from PIL import Image

from app.models.file import FileType
from app.schemas.file import FileFilledS
from app.services.media_service import MediaService


def generate_image_bytes(format: str = "PNG", size=(128, 128), color=(255, 0, 0)) -> io.BytesIO:
    img = Image.new("RGB", size, color=color)
    buf = io.BytesIO()
    img.save(buf, format=format)
    buf.seek(0)
    return buf

async def generate_db_image(media_service: MediaService) -> FileFilledS:
    valid_image = generate_image_bytes()

    file_db = await media_service.upload_avatar(file=valid_image, owner_id=uuid.uuid4(), content_type="image/png")

    assert file_db.url is not None

    return file_db

def check_image_url(url: str):
    parsed = urlparse(url)
    assert parsed.scheme in ("http", "https")
    assert parsed.netloc

    resp = requests.get(url)
    assert resp.status_code == 200
    assert resp.headers["Content-Type"].startswith("image/")

    img = Image.open(io.BytesIO(resp.content))
    img.verify()
    img = Image.open(io.BytesIO(resp.content))
    img.load()

async def generate_db_file(media_service: MediaService, owner_id: uuid.UUID, file_path: str = "test", visibility: Literal["public", "private"] = "public") -> FileFilledS:
    valid_image = generate_image_bytes()
    file_db = await media_service.upload(file=valid_image, file_type=FileType.AVATAR, content_type="image/png", file_path=file_path, owner_id=owner_id, visibility=visibility)
    return file_db
