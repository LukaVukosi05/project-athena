"""Past-paper metadata and allow-listed PDF delivery."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pypdf import PdfReader

from app.past_papers.catalog import PAPERS, QUESTION_GROUPS_2024

router = APIRouter()


@router.get("")
def list_papers() -> list[dict]:
    return [{"year": paper.year, "paper": paper.paper, "language": paper.language,
             "session": paper.session, "source": paper.source,
             "page_count": len(PdfReader(paper.path).pages),
             "view_url": f"/api/v1/past-papers/{paper.year}/paper-2"}
            for paper in PAPERS.values()]


@router.get("/2024/question-groups")
def question_groups_2024() -> dict:
    return QUESTION_GROUPS_2024


@router.get("/{year}/paper-2")
def view_paper(year: int) -> FileResponse:
    paper = PAPERS.get(year)
    if paper is None or not paper.path.is_file():
        raise HTTPException(status_code=404, detail="Past paper not found")
    return FileResponse(paper.path, media_type="application/pdf",
                        filename=f"DBE-NSC-Mathematics-P2-November-{year}.pdf",
                        content_disposition_type="inline")
