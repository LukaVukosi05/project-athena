"""Allow-listed local DBE Mathematics Paper 2 catalogue."""

from dataclasses import dataclass
from pathlib import Path

PAPER_ROOT = Path(__file__).resolve().parents[3] / "Paper 2 maths"


@dataclass(frozen=True)
class PastPaper:
    year: int
    filename: str
    paper: str = "Paper 2"
    language: str = "English"
    session: str = "November"
    source: str = "DBE NSC"

    @property
    def path(self) -> Path:
        return PAPER_ROOT / self.filename


PAPERS = {
    2016: PastPaper(2016, "Mathematics P2 Nov 2016 Eng - Copy.pdf"),
    2017: PastPaper(2017, "Mathematics P2 Nov 2017 Eng - Copy - Copy.pdf"),
    2019: PastPaper(2019, "Mathematics P2 Nov 2019 Eng - Copy.pdf"),
    2020: PastPaper(2020, "Mathematics P2 Nov 2020 Eng - Copy (2).pdf"),
    2021: PastPaper(2021, "Mathematics P2 Nov 2021 Eng - Copy.pdf"),
    2022: PastPaper(2022, "Mathematics P2 Nov 2022 Eng.pdf"),
    2023: PastPaper(2023, "Mathematics P2 Nov 2023 Eng.pdf"),
    2024: PastPaper(2024, "Mathematics P2 Nov 2024 Eng.pdf"),
}

QUESTION_GROUPS_2024 = {
    "statistics": {"questions": "1–2", "pages": "3–4", "marks": 20},
    "analytical-geometry": {"questions": "3–4", "pages": "5–6", "marks": 39},
    "trigonometry": {"questions": "5–8", "pages": "7–10", "marks": 50},
    "euclidean-geometry": {"questions": "9–11", "pages": "11–13", "marks": 41},
}
