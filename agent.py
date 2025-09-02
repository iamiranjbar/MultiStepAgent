import json, argparse, hashlib, sys, yaml
from tools import TOOLS
from prompts import SYSTEM_PROMPT
from llm import olllama_chat
from memory import JsonMemory

def _parse_json(raw: str):
    raw = raw.strip()
    # Best effort: find the first {...} block
    if not raw.startswith("{"):
        i = raw.find("{")
        if i != -1: 
            raw = raw[i:]
    return json.loads(raw)

# def run_single_step_agent(goal: str) -> str:
def run_agent(goal: str, config: dict) -> str:
    """
    Returns final answer or tool result (single step, no loops).
    """
    memory = JsonMemory(config["memory_path"])
    messages = [
        {"role":"system","content": SYSTEM_PROMPT},
        {"role":"user",  "content": f"Goal: {goal}"},
    ]
    seen_actions = set()

    for step in range(1, cfg["max_steps"] + 1):
        raw = olllama_chat(SYSTEM_PROMPT, f"Goal: {goal}\nDecide and respond in JSON.")
        try:
            plan = json.loads(raw.strip())
        except Exception as e:
            return f"PlannerError: invalid JSON from model: {e}\nRaw: {raw}"

        # Two valid shapes: {"action":"answer","final":"..."} or {"action":"tool","name":...,"input":...}
        action = plan.get("action")
        if action == "answer":
            return str(plan.get("final", "")).strip()

        if action == "tool":
            name = plan.get("name")
            tool_input = plan.get("input")

            if name not in TOOLS:
                return f"ToolError: unknown tool '{name}'."

            try:
                result = TOOLS[name](tool_input)
                return f"[{name} result] {result}"
            except Exception as e:
                return f"ToolExecutionError: {e}"

    return f"PlannerError: unsupported action. Got: {plan}"

if __name__ == "__main__":
    # Example goals you can try:
    goal = "Compute (sqrt(2)^2 + 10)/3 with the calculator."
    # goal = "Create a file 'notes.txt' with the text 'Hello agent' using write_file."
    # goal = "Read the file 'notes.txt' using read_file."
    # goal = "Briefly explain what a single-step agent is."
    # goal = "Compute (2+3)*5 using the calculator and give me just the number."
    print(run_single_step_agent(goal))
