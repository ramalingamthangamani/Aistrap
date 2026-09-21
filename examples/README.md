# Examples

What each template produces, and what to run next. The trees below are the real
output of `aistrap create`.

To generate all templates into `examples/generated/` (git-ignored) and try them
yourself:

```bash
python examples/generate_examples.py
```

---

## `python-ai` - basic Python AI project

```bash
aistrap create my-app
# or: aistrap create my-app --template python-ai
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
python -m app.main
pytest
```

`python -m app.main` prints the most common words in a sample text:

```
my-app: top words in the sample text
  data         2
  a            2
  machine      1
```

Start by replacing `word_frequencies` in `app/main.py` with your own logic.

---

## `fastapi` - FastAPI AI backend

```bash
aistrap create my-app --template fastapi
```

```
my-app/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
uvicorn app.main:app --reload
```

```console
$ curl http://127.0.0.1:8000/health
{"status":"ok","app":"my-app","version":"0.1.0"}
```

Interactive docs are at `/docs`. Add your endpoints in `app/api/routes.py`.

---

## `rag` - retrieval-augmented generation

```bash
aistrap create my-app --template rag
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── ingestion.py
│   ├── main.py
│   └── retrieval.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── documents/
│   └── getting-started.md
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
python -m app.main "What is retrieval-augmented generation?"
```

```console
$ python -m app.main "Why does chunking matter?"
Question: Why does chunking matter?

Answer:
... ## Why chunking matters Chunks that are too large waste context and dilute
the similarity score. Chunks that are too small lose the surrounding meaning.
Overlapping chunks help, because a sentence that falls on a boundary still
appears in full ...

Sources:
  - getting-started.md#2 (score 0.133)
```

The corpus is whatever is in `documents/`. Drop your own `.md`, `.txt` or `.rst`
files in there and ask again - no reindexing step, no API key.

Where to extend it:

| You want to | Change |
| --- | --- |
| Use embeddings or a vector database | `Retriever` in `app/retrieval.py` |
| Call a language model | `answer()` in `app/main.py`, using `build_prompt()` |
| Support PDFs or HTML | `TEXT_EXTENSIONS` and `load_documents` in `app/ingestion.py` |
| Change chunk size or how many passages are used | `.env` |

---

## `ml-project` - machine learning project

```bash
aistrap create my-app --template ml-project
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── predict.py
│   └── train.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── models/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
python -m app.train
python -m app.predict 5.1 3.5 1.4 0.2
```

```console
$ python -m app.train
Accuracy: 0.933

              precision    recall  f1-score   support

      setosa       1.00      1.00      1.00        10
  versicolor       0.90      0.90      0.90        10
   virginica       0.90      0.90      0.90        10

    accuracy                           0.93        30

Model saved to models/model.joblib

$ python -m app.predict 5.1 3.5 1.4 0.2
Prediction: setosa (confidence 0.981)
```

To use your own data, put it in `data/` and rewrite `load_dataset()` in
`app/train.py`. It only has to return features, labels, class names and feature
names - everything else keeps working.

---

## `ai-agent` - autonomous AI agent

```bash
aistrap create my-app --template ai-agent
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── main.py
│   └── tools.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
python -m app.main "Calculate 25 * 4 and tell me what is AI"
```

---

## `ai-fullstack` - fullstack AI app with Web UI

```bash
aistrap create my-app --template ai-fullstack
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── static/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` to interact with the responsive web interface.

---

## `mcp-server` - Model Context Protocol server

```bash
aistrap create my-app --template mcp-server
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── protocol.py
│   └── server.py
├── config/
│   └── .gitkeep
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
python -m app.main
```

---

## `multimodal` - multimodal vision & media pipeline

```bash
aistrap create my-app --template multimodal
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── vision.py
├── config/
│   └── .gitkeep
├── data/
│   └── .gitkeep
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
python -m app.main
```

---

## `chat-stream` - streaming conversational AI (SSE)

```bash
aistrap create my-app --template chat-stream
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── sessions.py
├── config/
│   └── .gitkeep
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## `llm-eval` - LLM evaluation & benchmark harness

```bash
aistrap create my-app --template llm-eval
```

```
my-app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── evaluator.py
│   ├── main.py
│   └── metrics.py
├── config/
│   └── .gitkeep
├── data/
│   └── golden_dataset.json
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

```bash
cd my-app
pip install -r requirements.txt
python -m app.main
```

---

## Common usage

```bash
# Create into a directory other than the current one
aistrap create my-app --directory ~/projects

# Write into an existing non-empty directory (asks first unless --force)
aistrap create existing-dir --force

# See what is available, and check your environment
aistrap list
aistrap doctor
```
