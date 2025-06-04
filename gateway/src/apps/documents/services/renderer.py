from io import BytesIO
from fastapi import Depends
from typing import Annotated, Protocol, Self
import aiohttp
from gateway.src.apps.documents.schemas.services.renderer import (
    RenderRequest,
    RenderResponse,
)
from shared.repositories.s3 import S3Repository
from PIL import Image


class RenderService(Protocol):
    async def render(self: Self, data: RenderRequest) -> RenderResponse: ...


class RenderServiceImpl(RenderService):
    def __init__(self: Self, render_repo: RenderRepository, s3_repo: S3Repository):
        self.s3_repo = s3_repo
        self.render_repo = render_repo

    async def render(self: Self, data: RenderRequest) -> RenderResponse:
        url = await self.s3_repo.get_download_url(data.cleaned_url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                image_data = BytesIO(await resp.content.read())
                image = Image.open(image_data)

        rendered = self.render_repo.render(image, data.frames)
        buffer = BytesIO()
        rendered.save(buffer, format="PNG")
        filename = await self.s3_repo.upload(buffer.read())
        rendered_url = await self.s3_repo.get_download_url(filename)
        return RenderResponse(rendered_url=rendered_url)


def render_service_factory(repo: RenderRepositoryDep):
    return RenderServiceImpl(repo)


RenderServiceDep = Annotated[RenderService, Depends(render_service_factory)]
