# PromptIQ — The AI Prompt Engineering Laboratory

PromptIQ is a production-grade, interactive prompt engineering learning and productivity web platform. It helps developers, researchers, and AI practitioners understand, evaluate, systematically improve, and empirically compare Large Language Model prompts using Google Gemini and modern prompt design architecture.

---

## 🌟 Key Capabilities

### 1. 🔬 Prompt Analyzer
- **Multidimensional Diagnostic Evaluation**: Analyzes prompts across 6 core criteria:
  - **Clarity**: Freedom from ambiguity and vagueness.
  - **Context**: Domain background, technical environment, and audience grounding.
  - **Specificity**: Concrete metrics, quantitative limits, and bounded scope.
  - **Task Definition**: Unambiguous directive verbs and primary deliverables.
  - **Output Format**: Structural specifications (JSON, Markdown tables, bullet hierarchies).
  - **Constraints**: Negative boundaries, guardrails, and exclusions.
- **Objective Scoring (0–100)**: Evaluates weighted scores with explicit justification—no arbitrary numbers.
- **Flaw Detection & Impact Analysis**: Identifies architectural weaknesses and explains *why* each flaw impairs model performance.
- **Actionable Guidance**: Delivers concrete recommendations to remediate weaknesses.

### 2. ✨ Prompt Optimizer
- **Intelligent Refactoring**: Rewrites naive prompts into production-grade instructions while preserving original intent.
- **Injected Architectural Elements**:
  - Authoritative expert persona / role.
  - Crisp task definition.
  - Necessary operational context.
  - Deterministic output format requirements.
  - Negative constraints and guardrails.
- **Side-by-Side Prompt Diff**: Inspect original vs. engineered prompts simultaneously.

### 3. 📋 Prompt Improvement Explanation
- **Granular Change Table**: Provides a structured breakdown mapping each change:
  `Original Element | Improvement | Reason`
- Grounded in prompt engineering principles.

### 4. ⚖️ Empirical Comparison Lab
- **Dual Inference Execution**: Runs the original and optimized prompts against Google Gemini simultaneously under identical sampling temperatures.
- **Side-by-Side Output Inspection**: Displays both real model generations side by side.
- **Evidence-Based Variance Analysis**: Compares observable output differences without subjective claims—validating improvements strictly based on empirical response data.

### 5. 📚 Prompt Template Library
- **Pre-Built Starter Templates** spanning 6 domains:
  - **Learning** (Complex explanations, historical perspectives)
  - **Coding** (Async refactors, SQL query optimization)
  - **Research** (Emerging tech synthesis, architecture benchmarking)
  - **Content Writing** (Developer launch announcements, executive newsletters)
  - **Data Analysis** (Churn cohort analysis, A/B testing frameworks)
  - **Interview Preparation** (System design mocks, executive STAR stories)
- **One-Click Loading**: Instantly load any template into the Analyzer, Optimizer, or Comparison Lab.

### 6. 🕒 Session History & Vault
- **Automatic State Tracking**: Persists tested prompts, scores, and optimized versions in Streamlit session state.
- **One-Click Reusability**: Re-run or cross-load prior prompts into any laboratory view.
- **History Management**: Clear session history anytime with a single click.

### 7. 🎓 Educational Academy
- **In-Depth Guides**:
  - **Role Prompting**: Identity priming and domain perspective.
  - **Context Provision**: Background state and audience grounding.
  - **Specificity & Precision**: Eliminating ambiguous adjectives.
  - **Constraints & Guardrails**: Negative boundaries and scope caps.
  - **Output Formatting**: Schemas, headers, and machine-readable layouts.
  - **Few-Shot Prompting**: Pattern priming with input-output exemplars.
  - **Chain-of-Thought Prompting**: Cognitive decomposition—with explicit guidance to request concise reasoning summaries or intermediate steps rather than unparseable internal monologue.

---

## 🛠️ Technology Stack

- **Frontend & Web Framework**: [Streamlit](https://streamlit.io/) (v1.35+)
- **LLM Engine**: Google Gemini API powered by the official [`google-genai`](https://github.com/googleapis/python-genai) SDK
- **Data Validation & Typing**: [Pydantic](https://docs.pydantic.dev/) v2
- **Environment Management**: `python-dotenv`
- **Recommended Model**: `gemini-3.8-flash` (also supports `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`)

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+ installed
- A Google Gemini API key ([Get a free key at Google AI Studio](https://aistudio.google.com/app/apikey))

### 2. Clone or Navigate to the Repository
```bash
git clone https://github.com/your-username/promptiq.git
cd promptiq
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key
You can configure your API key through **any** of the following methods:

#### Option A: Environment Variable (Recommended for Local Dev)
**macOS/Linux**:
```bash
export GEMINI_API_KEY="your_api_key_here"
```
**Windows (PowerShell)**:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

#### Option B: Local `.env` File
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_api_key_here
```

#### Option C: In-App Sidebar
When launching PromptIQ, you can paste your API key directly into the secure masked password field in the sidebar.

> **Note**: If no API key is supplied, PromptIQ automatically runs in **Offline / Demonstration Mode**, allowing you to test all features and UI views with intelligent heuristics without crashing.

### 5. Launch the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deployment on Streamlit Community Cloud

PromptIQ is designed for seamless deployment on Streamlit Community Cloud:

1. Push this repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app**, select your repository, branch, and set `app.py` as the **Main file path**.
4. In **Advanced settings** -> **Secrets**, add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
5. Click **Deploy!**

---

## 🧪 Running Automated Tests

PromptIQ includes a test suite covering schema validation, heuristic engines, state management, and template verification:

```bash
python -m unittest tests/test_promptiq.py
```

---

## 📂 Project Architecture

```
PROMPTIQ/
├── .streamlit/
│   └── config.toml           # Sleek dark-mode theme & server configuration
├── core/
│   ├── __init__.py
│   ├── analyzer.py           # Multi-dimensional rubric analyzer wrapper
│   ├── comparator.py         # Dual prompt execution and comparative synthesis
│   ├── gemini_service.py     # Official google-genai client wrapper & offline engine
│   ├── optimizer.py          # Intent-preserving prompt refactorer
│   └── schemas.py            # Pydantic structured output models
├── data/
│   ├── __init__.py
│   ├── education.py          # Pedagogical prompt engineering lessons & examples
│   └── templates.py          # Domain-categorized prompt template catalog
├── tests/
│   └── test_promptiq.py      # Automated unit & integration tests
├── utils/
│   ├── __init__.py
│   ├── state.py              # Session state, history vault, and cross-view routing
│   └── ui_helpers.py         # Custom CSS badges, metric cards, and layout helpers
├── views/
│   ├── __init__.py
│   ├── analyzer_view.py      # Diagnostic quality scoring view
│   ├── comparator_view.py    # Side-by-side Gemini comparison lab
│   ├── education_view.py     # Educational academy hub
│   ├── history_view.py       # Session history and vault view
│   ├── optimizer_view.py     # Side-by-side prompt optimizer view
│   └── templates_view.py     # Categorized template explorer
├── .env.example              # Example environment configuration
├── .gitignore                # Production Python & Streamlit gitignore
├── app.py                    # Main Streamlit application entry point
├── README.md                 # Complete documentation & deployment guide
└── requirements.txt          # Python dependencies
```

---

## 📄 License
MIT License. Built for prompt engineers, researchers, and builders.
