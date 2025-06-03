from typing import Annotated
from gateway.src.apps.documents.services.ocr import OCRService, OCRServiceDep
from apps.documents.schemas.router import (
    FindAreasRequest,
    FindAreasResponse,
    TranslatePageKnownAreasRequest,
    TranslatePageResponse,
)
from fastapi import APIRouter, UploadFile
from gateway.src.apps.documents.services.translation import (
    TranslationService,
    TranslationServiceDep,
)
from shared.services.s3 import S3Service, S3ServiceDep
from apps.documents.schemas.services.documents import Frame

router = APIRouter(prefix="ocr")


@router.post("find_areas", response_model=FindAreasResponse)
async def find_areas(
    data: FindAreasRequest,
    ocr: Annotated[OCRServiceDep, OCRServiceDep],
):
    return await ocr.find_areas(data)


@router.post("translate/known_areas", response_model=TranslatePageResponse)
async def translate_page_known_areas(
    translated_image: UploadFile,
    file_data: TranslatePageKnownAreasRequest,
    s3: Annotated[S3Service, S3ServiceDep],
    translation: Annotated[TranslationService, TranslationServiceDep],
    cleaner: Annotated[CleanerService, CleanerServiceDep],
    renderer: Annotated[RendererService, RendererServiceDep],
) -> TranslatePageResponse:
    filename = await s3.upload(await translated_image.read())
    image_url = await s3.get_url(filename)
    translated_text = await translation.translate(file_data)
    cleaned_image_url = await cleaner.clean(image_url)
    translated_image = await renderer.render(cleaned_image_url, translated_text)
    translated_filename = await s3.upload(translated_image)
    translated_url = await s3.get_url(translated_filename)
    return TranslatePageResponse(translated_url=translated_url)


@router.post("translate/detect_areas", response_model=TranslatePageResponse)
async def translate_page_detect_areas(
    file: UploadFile,
    ocr: Annotated[OCRService, OCRServiceDep],
    s3: Annotated[S3Service, S3ServiceDep],
    translation: Annotated[TranslationService, TranslationServiceDep],
    renderer: Annotated[RendererService, RendererServiceDep],
) -> TranslatePageResponse:
    filename = await s3.upload(data.file)
    url = await s3.get_url(filename)
    text_areas = await ocr.find_areas(url)
    translated_text = await translation.translate(text)
    image = await renderer.render(url, translated_text)
    translated_filename = s3.upload(image)
    return await s3.get_url(translated_filename)
