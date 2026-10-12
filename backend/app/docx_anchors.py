"""Paragraph ids (`w14:paraId`) for review-comment anchors.

A review comment points at the text it's about by paragraph id plus the quoted text (see
db.py's review_comments table, and ReviewComments.tsx, which hands those to the editor's
scrollToAnchor). Word writes a w14:paraId on every paragraph, but python-docx doesn't, so a
generated report has none -- and the editor can't address a paragraph without one. This
gives every body paragraph a unique id before a revision is frozen for review, keeping the
ones it already has.
"""

import io
import secrets
import zipfile

from lxml import etree

_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_W14 = "http://schemas.microsoft.com/office/word/2010/wordml"
_PARA_ID = f"{{{_W14}}}paraId"
_DOCUMENT = "word/document.xml"


def _valid(para_id: str) -> bool:
    # Word's rule: 8 hex digits, below 0x80000000.
    try:
        return len(para_id) == 8 and int(para_id, 16) < 0x80000000
    except ValueError:
        return False


def ensure_paragraph_ids(docx: bytes) -> bytes:
    """`docx` with a w14:paraId on every body paragraph, unique within the body. Returns the
    input unchanged when there's nothing to add."""
    with zipfile.ZipFile(io.BytesIO(docx)) as src:
        root = etree.fromstring(src.read(_DOCUMENT))
        seen: set[str] = set()
        changed = False
        for paragraph in root.iter(f"{{{_W}}}p"):
            para_id = (paragraph.get(_PARA_ID) or "").upper()
            # A paragraph split in an editor can come out with a copy of its neighbour's id.
            if not _valid(para_id) or para_id in seen:
                para_id = _new_id(seen)
                paragraph.set(_PARA_ID, para_id)
                changed = True
            seen.add(para_id)
        if not changed:
            return docx
        document = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
            for item in src.infolist():
                dst.writestr(item, document if item.filename == _DOCUMENT else src.read(item.filename))
    return out.getvalue()


def _new_id(taken: set[str]) -> str:
    while True:
        para_id = f"{secrets.randbelow(0x7FFFFFFF) + 1:08X}"
        if para_id not in taken:
            return para_id
