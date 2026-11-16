"""Compare API schema, lesson/reveal payloads and private banks against a Git ref.

Run from the repository root: python tools/verify_runtime_parity.py
Uses two isolated subprocesses and a disposable worktree; never reads a local DB.
The temporary comparison user is premium so entitlement does not hide content.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline", default="a393b6c7b3ff883fc16c5f5c9922f5a0be660fe9"
    )
    parser.add_argument(
        "--content-only",
        action="store_true",
        help="Allow intentional API schema changes; compare curriculum payloads only",
    )
    parser.add_argument("--snapshot", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.snapshot:
        snapshot(args.snapshot)
        return
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="athena-parity-") as directory:
        temporary = Path(directory)
        baseline = temporary / "baseline"
        subprocess.run(
            ["git", "worktree", "add", "--detach", str(baseline), args.baseline],
            cwd=root,
            check=True,
            capture_output=True,
        )
        try:
            for label, source in (("baseline", baseline), ("current", root)):
                environment = dict(
                    os.environ,
                    PYTHONPATH=str(source / "backend"),
                    ATHENA_JWT_SECRET="local-parity-comparison-only",
                    ATHENA_DATABASE_URL="sqlite://",
                    ATHENA_ENVIRONMENT="development",
                    ATHENA_UNLOCK_ALL_LESSONS="false",
                )
                subprocess.run(
                    [
                        sys.executable,
                        str(Path(__file__).resolve()),
                        "--snapshot",
                        str(temporary / (label + ".json")),
                    ],
                    cwd=temporary,
                    env=environment,
                    check=True,
                )
            before = json.loads((temporary / "baseline.json").read_text())
            after = json.loads((temporary / "current.json").read_text())
            if args.content_only:
                before.pop("routes", None)
                after.pop("routes", None)
            if before != after:
                for group in before:
                    if before[group] != after[group]:
                        if isinstance(before[group], dict):
                            changed = [
                                key
                                for key in before[group].keys() | after[group].keys()
                                if before[group].get(key) != after[group].get(key)
                            ]
                            print(f"Changed {group}: {changed}")
                        else:
                            print(f"Changed {group}")
                raise SystemExit("Runtime parity FAILED")
            print("Runtime parity PASSED: all selected outputs are identical.")
        finally:
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(baseline)],
                cwd=root,
                check=True,
                capture_output=True,
            )


def snapshot(output: Path) -> None:
    """Resolve app imports against PYTHONPATH in an isolated subprocess."""
    from fastapi.encoders import jsonable_encoder
    from fastapi import HTTPException
    from app.curriculum.repository import curriculum_repository as repository
    from app.api.v1.lessons import get_lesson, reveal_worked_example
    from app.api.v1.practice import ASSESSMENT_BANKS
    from app.practice.catalog import PRACTICE_BANKS
    from app.main import app
    from app.db.models.user import User

    def digest(value):
        return hashlib.sha256(
            json.dumps(
                jsonable_encoder(value), sort_keys=True, ensure_ascii=False
            ).encode()
        ).hexdigest()

    result = {
        "lessons": {},
        "reveals": {},
        "banks": {},
        "routes": digest(app.openapi()),
    }
    user = User(id=1, is_premium=True)
    for grade in repository.list_grades():
        for topic in grade.topics:
            for subtopic in topic.subtopics:
                for lesson in subtopic.lessons:
                    try:
                        payload = get_lesson(lesson.id, user=user)
                        result["lessons"][lesson.id] = digest(payload)
                        for question in lesson.whiteboard_questions:
                            try:
                                value = reveal_worked_example(
                                    lesson.id, question.id, user=user
                                )
                            except HTTPException as e:
                                value = {"status": e.status_code, "detail": e.detail}
                            result["reveals"][lesson.id + "/" + question.id] = digest(
                                value
                            )
                    except HTTPException as e:
                        result["lessons"][lesson.id] = digest(
                            {"status": e.status_code, "detail": e.detail}
                        )
    for key, bank in PRACTICE_BANKS.items():
        result["banks"][key] = digest(
            {
                "practice": [q.model_dump() for q in bank],
                "assessment": ASSESSMENT_BANKS.get(key),
            }
        )
    with open(output, "w", encoding="utf-8") as f:
        json.dump(result, f, sort_keys=True)
    print(
        {
            key: len(value) if isinstance(value, dict) else value
            for key, value in result.items()
        }
    )


if __name__ == "__main__":
    main()
