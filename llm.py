import subprocess

def ollama_chat(model: str, messages: list[dict], num_ctx=4096, temperature=0.2) -> str:
    """
    Return the model's raw text using ollama model.
    """
    prompt = "\n".join(f"{m['role'].upper()}:\n{m['content']}" for m in messages)
    out = subprocess.run(
        ["ollama", "run", model, f"num_ctx={num_ctx}", f"temperature={temperature}"], 
        input=prompt.encode("utf-8"), 
        capture_output=True,
        check=False,
    )
    return out.stdout.decode("utf-8", errors="ignore")
