"""Check the actual Athena server for the Grade 8 preview-to-teaching handoff.

Usage: python tools/diagnose_grade8_example_loading.py http://127.0.0.1:8050 g8-algebraic-equations-10
"""

import json
import sys
import urllib.error
import urllib.request


def request(base: str, path: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        base.rstrip("/") + path,
        data=data,
        headers={"Content-Type": "application/json"} if data else {},
        method="POST" if data else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", errors="replace")


def main() -> int:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8050"
    lesson_id = sys.argv[2] if len(sys.argv) > 2 else "g8-algebraic-equations-10"
    try:
        status, html = request(base, "/lesson.html")
        if status != 200:
            print(f"Lesson page HTTP {status}: {html[:160]}")
            return 1
        version = "whiteboard-v10" if "lesson-block-renderer.js?v=whiteboard-v10" in html else "older loader asset"
        print(f"Page served: HTTP {status}; {version}")
        status, script = request(base, "/js/lessons/lesson-block-renderer.js")
        diagnosis_supported = "diagnosis?'diagnose':'reveal'" in script
        print(f"Loader served: HTTP {status}; Lesson 10 diagnosis supported: {diagnosis_supported}")
        if lesson_id.endswith("-10") and not diagnosis_supported:
            print("FAIL: Browser is receiving the old loader. Restart the correct checkout and reload the page.")
            return 1
        status, raw = request(base, f"/api/v1/lessons/{lesson_id}")
        if status != 200:
            print(f"Lesson API HTTP {status}: {raw[:240]}")
            return 1
        questions = json.loads(raw)["whiteboard_questions"]
        first = questions[0]
        preview_steps = len(first["whiteboard"]["steps"])
        authored_steps = first.get("total_step_count", "missing")
        print(f"First example {first['id']}: preview={preview_steps}, authored={authored_steps}")
        endpoint = "diagnose" if lesson_id.endswith("-10") else "reveal"
        body = {"first_error_and_repair": "The first invalid change fails to preserve equality; correct both sides."} if endpoint == "diagnose" else {}
        status, raw = request(base, f"/api/v1/lessons/{lesson_id}/questions/{first['id']}/{endpoint}", body)
        if status != 200:
            print(f"Full example HTTP {status}: {raw[:240]}")
            return 1
        full_steps = len(json.loads(raw)["whiteboard"]["steps"])
        print(f"Full example: HTTP 200; steps={full_steps}")
        if full_steps <= preview_steps:
            print("FAIL: The server did not deliver the authored teaching steps.")
            return 1
        print("PASS: This server delivers the full example. If the browser still shows one step, inspect its Console/Network request and hard-reload this page.")
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"FAIL: Could not inspect {base}: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
