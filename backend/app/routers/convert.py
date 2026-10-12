"""Document conversion used by the report editor's File > Export > PDF and File > Print."""

from fastapi import APIRouter, HTTPException, Request, Response
from starlette.concurrency import run_in_threadpool

from ..docx_pdf import PdfConversionError, docx_to_pdf

router = APIRouter(prefix="/api/convert", tags=["convert"])

MAX_DOCX_BYTES = 50 * 1024 * 1024


async def read_docx_body(request: Request) -> bytes:
    body = await request.body()
    if len(body) > MAX_DOCX_BYTES:
        raise HTTPException(status_code=413, detail="That document is too large (50 MB max).")
    if not body.startswith(b"PK"):  # .docx is a zip archive
        raise HTTPException(status_code=422, detail="That isn't a .docx file.")
    return body


@router.post("/docx-to-pdf")
async def convert_docx_to_pdf(request: Request):
    docx = await read_docx_body(request)
    try:
        pdf = await run_in_threadpool(docx_to_pdf, docx)
    except PdfConversionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return Response(content=pdf, media_type="application/pdf")
