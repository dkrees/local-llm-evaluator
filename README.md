# Local LLM Evaluation Framework

A Python framework for testing and evaluating local language models running through LM Studio or similar OpenAI-compatible endpoints. This tool allows you to systematically evaluate model performance across different types of tasks including simple Q&A, rationale-based reasoning, and text summarization.

## Features

- Test local models via OpenAI-compatible API (LM Studio, etc.)
- Multiple evaluation types: simple questions, rationale-based answers, and summarization
- Support for both OpenAI and Anthropic as evaluators
- Configurable test parameters (number of tests, models, datasets)
- CSV export of detailed results with metrics
- Performance tracking (response time, token usage)

## Setup

### 1. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API keys
Copy the example environment file and add your API keys:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Note:** You need at least one API key for the evaluator service. The subject model runs locally through LM Studio.

### 4. Start LM Studio
- Download and start [LM Studio](https://lmstudio.ai/)
- Load your desired model
- Start the local server (default: http://127.0.0.1:1234/v1)

## Usage

### Configuration
Edit the configuration variables in `main.py`:

```python
subject_model = "lfm2-1.2b"           # Model name in LM Studio
evaluator = "openai"                  # "openai" or "anthropic"
evaluator_model = "gpt-4o-mini"       # Evaluator model
number_of_tests = 3                   # Tests per question
dataset = "test_data/summarise_1.txt" # Path to test data
evaluation_type = EvaluationType.SUMMARISE  # Test type
```

### Run evaluation
```bash
python main.py
```

### Test data formats
- **Summarization**: Plain text files (prefix: `summarise_`)
- **Q&A pairs**: Format with `Q: question` and `A: answer` blocks (prefix: `questions_`)
- **Questions only**: Format with `Q: question` only (prefix: `questions_`)

## Evaluation Types

1. **SIMPLE_QUESTION**: Short, accurate responses
2. **RATIONALE**: Detailed answers with reasoning
3. **SUMMARISE**: Text summarization tasks

## Output

Results are exported to `test_results.csv` with detailed metrics including:
- Evaluation scores
- Response times
- Token usage (prompt, completion, total)
- Per-question and overall averages

## Deactivate environment
```bash
deactivate
```