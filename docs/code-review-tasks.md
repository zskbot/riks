# Code review follow-up tasks

This review identifies four focused maintenance tasks from the current source tree.

## 1. Typo cleanup: normalize the project name in the README

- **Area:** `README.md`
- **Problem:** The README opens with `Clauderiks`, while the code and feature list consistently describe the product as `Risk AI`. The stray name makes the project identity look accidental and harder to search.
- **Task:** Replace the opening label with a clear Risk AI tagline, then scan the README for any remaining accidental name drift.
- **Suggested acceptance check:** `rg -n "Clauderiks|Risk AI" README.md`

## 2. Bug fix: add or package the missing backend modules

- **Area:** `backend/main.py`, `backend/api/routes.py`, and `backend/agents/*.py`
- **Problem:** The backend imports `config.settings`, `models`, `memory`, `tools`, and `agents.llm_client`, but those modules are not present in the tracked `backend/` tree. Starting the FastAPI app will fail before any route can respond.
- **Task:** Add the missing modules or update imports to point at existing implementations. Include minimal settings, request/response models, memory storage, tool adapters, and an Ollama client stub/implementation so the app can import cleanly.
- **Suggested acceptance check:** `PYTHONPATH=backend python -c "from main import app; print(app.title)"`

## 3. Comment/documentation drift: align README claims with implemented capabilities

- **Area:** `README.md` and route docstrings in `backend/api/routes.py`
- **Problem:** The README describes an agent that can read projects, write code, run Docker-sandboxed commands, use GitHub integration, remember context, and perform RAG. The current chat route only sends the message to Ollama and returns `tool_calls=[]`; tool routes exist as API endpoints but are not orchestrated from chat.
- **Task:** Split the README into “implemented now” and “roadmap” sections, and update route docstrings to clarify that `/api/chat` is currently LLM-only until tool routing is wired in.
- **Suggested acceptance check:** `rg -n "tool calling|RAG|memory|tool_calls|LLM-only|roadmap" README.md backend/api/routes.py`

## 4. Testing workflow improvement: add backend import smoke tests and frontend CI checks

- **Area:** repository test/CI setup
- **Problem:** There is no tracked test suite or CI workflow that exercises the backend imports, API contract, or frontend build. The existing missing-module bug would be caught by even a one-line import smoke test.
- **Task:** Add a small pytest suite for backend import and route smoke tests, add a frontend type/build check, and wire both into a single CI workflow or documented local check script.
- **Suggested acceptance check:** `pytest backend/tests && npm --prefix frontend run build`
