from typing import Annotated
from gateway.src.apps.documents.services.ocr import OCRService, OCRServiceDep
from gateway.src.apps.documents.schemas.routers.documents import (
    FindAreasRequest,
    FindAreasResponse,
    TranslatePageRequest,
    TranslatePageResponse,
)
from fastapi import APIRouter, Depends

router = APIRouter(prefix="ocr")


@router.post("find_areas", response_model=FindAreasResponse)
async def find_areas(
    data: FindAreasRequest,
    ocr: Annotated[OCRServiceDep, OCRServiceDep],
):
    return await ocr.find_areas(data)


@router.post("translate", response_model=TranslatePageResponse)
async def translate_page(
    data: TranslatePageRequest,
    ocr: Annotated[OCRService, OCRServiceDep],
    s3: Annotated[S3Service, S3ServiceDep],
    translation: Annotated[TranslationService, TranslationService],
) -> TranslatePageResponse:
    filename = await s3.upload(data.file)
    url = await s3.get_url(filename)
    text = await ocr.scan(url)
    translated_text = await translation.translate(text)
    image = await renderer.render(url, translated_text)
    translated_filename = s3.upload(image)
    return await s3.get_url(translated_filename)
