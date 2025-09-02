# Multi Step Agent
Lightweight local AutoGPT-style agent built with Python and Ollama — supports multi-step planning, tool use, and JSONL memory with a simple CLI.

An agent that can complete a task in multiple steps using directly call LLM or using tools.
- The model can either ANSWER or CALL ONE TOOL at each step.
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
### You should call them by CLI!
```bash
- python agent.py --goal "Compute (sqrt(2)^2 + 10)/3 with the calculator."
- python agent.py --goal "Create a file 'notes.txt' with the text 'Hello agent' using file_write."
- python agent.py --goal "Read the file 'notes.txt' using file_read."
- python agent.py --goal "Briefly explain what a single-step agent is."
- python agent.py --goal "Compute (2+3)*5 using the calculator and give me just the number."
```
