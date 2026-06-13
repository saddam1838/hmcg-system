<div align="center">

# 🧠 Hierarchical Metacognitive Code Generation (HMCG)

### *A Multi-Agent Framework for Robust, Symmetry-Aware Autonomous Code Generation*

[![Python Version](https://img.shields.io/badge/Python-3.10+-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Research-success)]()

**Proactive Planning • Collaborative Validation • Reactive Debugging • Symmetry-Aware Reasoning**

</div>

---

# 📑 Table of Contents

* [Overview](#-overview)
* [Features](#-features)
* [Architecture](#-architecture)
* [Tech Stack](#-tech-stack)
* [Installation](#-installation)
* [Usage](#-usage)
* [Project Structure](#-project-structure)
* [Evaluation](#-evaluation)
* [Future Work](#-future-work)
* [Authors](#-authors)

---

# 🚀 Overview

Hierarchical Metacognitive Code Generation (HMCG) is a research-oriented multi-agent framework designed to improve autonomous code generation through structured planning, collaborative validation, and reactive debugging.

Instead of relying on a single LLM response, HMCG decomposes the generation process into multiple specialized agents that reason, validate, critique, and refine generated solutions before execution.

The framework also explores symmetry-aware validation concepts inspired by multi-agent learning, encouraging structurally robust solutions beyond simple syntactic correctness.

---

# ✨ Features

* 🧠 Strategic planning before code generation
* 👥 Multi-agent collaborative validation
* 🔍 Metacognitive reasoning pipeline
* ⚡ Reactive debugging and iterative repair
* 📋 JSON-based planning artifacts
* 🧩 Symmetry-aware validation concepts (PI/PE)
* 💻 Multi-language code generation support
* 📊 Streamlit-based interactive interface
* 📁 Automatic task metadata generation
* 🔄 Modular and extensible architecture

---

# 🏗️ Architecture

```mermaid
graph TD

A[User Task] --> B[Strategic Planner]

B --> C[Observer Agent]

C --> D[Technical Coder]

D --> E[Observer Agent]

E --> F[Reactive Debugger]

F --> G{Execution Successful?}

G -->|No| F

G -->|Yes| H[Final Generated Code]
```

## Pipeline

### 1. Strategic Planner

* Analyzes user objectives
* Produces structured planning artifacts
* Defines implementation strategy
* Identifies constraints and success criteria

---

### 2. Observer (Planning Validation)

* Reviews planning completeness
* Validates reasoning consistency
* Performs structural assessment
* Evaluates symmetry-aware considerations

---

### 3. Technical Coder

* Converts validated plans into executable code
* Generates implementation details
* Produces documentation-ready output
* Supports multiple programming languages

---

### 4. Observer (Code Validation)

* Reviews generated implementation
* Compares code against planning objectives
* Detects inconsistencies
* Identifies structural weaknesses

---

### 5. Reactive Debugger

* Executes generated code
* Detects runtime issues
* Repairs implementation errors
* Iteratively refines solutions

---

# 🛠️ Tech Stack

| Category      | Technology                                                    |
| ------------- | ------------------------------------------------------------- |
| Language      | Python 3.10+                                                  |
| Frontend      | Streamlit                                                     |
| Backend       | Python                                                        |
| API           | Hugging Face Inference API                                    |
| LLM Support   | DeepSeek Models                                               |
| Visualization | Plotly                                                        |
| Data Format   | JSON                                                          |
| Concepts      | Multi-Agent Systems, Metacognition, Symmetry-Aware Validation |

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/saddam1838/hmcg-system.git

cd hmcg-system
```

## Create Virtual Environment

Linux/macOS

```bash
python -m venv venv

source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment

Create:

```text
.env
```

Example:

```env
HUGGINGFACE_TOKEN=your_token_here

MODEL_NAME=your_model_name

API_URL=your_api_endpoint
```

---

# 💻 Usage

## Streamlit UI

```bash
streamlit run ui/streamlit_app.py
```

Open:

```
http://localhost:8501
```

---

## Command Line

```bash
python main.py \
  --task "Create a sorting algorithm" \
  --constraints "Use Python"
```

---

# 📂 Project Structure

```text
hmcg-system/

├── agents/
│   ├── strategic_planner.py
│   ├── collaborative_observer.py
│   ├── technical_coder.py
│   ├── reactive_debugger.py
│   └── metacognitive_orchestrator.py
│
├── utils/
│   ├── llm_handler.py
│   └── code_executor.py
│
├── ui/
│   └── streamlit_app.py
│
├── generated_code/
│
├── saved_tasks/
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

---

# 📊 Evaluation

This repository serves as a research prototype exploring hierarchical metacognitive code generation with specialized agents.

If benchmark experiments are included in the project, they should document:

* Evaluation methodology
* Benchmark tasks
* Baseline comparisons
* Execution success rates
* Debugging iterations
* Structural validation metrics
* Reproducibility details

For published experimental results, please refer to the accompanying research documentation or paper.

---

# 🔮 Future Work

* Reinforcement learning enhanced planning
* Distributed multi-agent orchestration
* Formal verification integration
* Advanced reasoning memory
* Self-improving agent collaboration
* Expanded benchmark evaluation
* Docker deployment
* Kubernetes support

---

# 📸 Demo

You can include screenshots here after implementation.

```markdown
![Dashboard](assets/dashboard.png)

![Planning](assets/planning.png)

![Generated Code](assets/generated_code.png)
```

---

# 👨‍💻 Authors

**Muhammad Saddam**

* GitHub: https://github.com/saddam1838
* LinkedIn: https://linkedin.com/in/muhammad-saddam-185a80215

---


<div align="center">

Built with ❤️ as part of an MS Artificial Intelligence research initiative.

If you find this project useful, consider giving it a ⭐ on GitHub.

</div>
