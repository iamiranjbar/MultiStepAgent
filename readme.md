# Multi Step Agent
Lightweight local AutoGPT-style agent built with Python and Ollama — supports multi-step planning, tool use, and JSONL memory with a simple CLI.

An agent that can complete a task in a single step or use one external tool to solve it.
- The model can either ANSWER or CALL ONE TOOL, then stop.
- Includes a tiny toolset: calculator, read_file, write_file
- Swap the `llm_call()` implementation for OpenAI, Ollama, etc.

## LLM Call

### Ollama
- You can see in the code.

### OpenAI (requires OPENAI_API_KEY in environment):
```python
from openai import OpenAI
client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0,
    messages=[{"role":"system","content":system},
        {"role":"user","content":user}]
)
return resp.choices[0].message.content
```

## Example tasks/Goals
- Compute (sqrt(2)^2 + 10)/3 with the calculator.
- Create a file 'notes.txt' with the text 'Hello agent' using file_write.
- Read the file 'notes.txt' using file_read.
- Briefly explain what a single-step agent is.
- Compute (2+3)*5 using the calculator and give me just the number.
