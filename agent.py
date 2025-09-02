import json, argparse, hashlib, sys, yaml
from tools import TOOLS
from prompts import SYSTEM_PROMPT
from llm import ollama_chat
from memory import JsonMemory

def _parse_json(raw: str):
    raw = raw.strip()
    # Best effort: find the first {...} block
    if not raw.startswith("{"):
        i = raw.find("{")
        if i != -1: 
            raw = raw[i:]
    return json.loads(raw)

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

    for step in range(1, config["max_steps"] + 1):

        raw = ollama_chat(
            config["model"], messages,
            num_ctx=config["num_ctx"], temperature=config["temperature"]
        )

        try:
            plan = _parse_json(raw)
            print(plan)
        except Exception as e:
            return f"ParseError at step {step}. Raw:\n{raw[:500]}"

        memory.add({"step": step, "plan": plan})
        # Two valid shapes: {"action":"answer","final":"..."} or {"action":"tool","name":...,"input":...}
        action = plan.get("action")
        if action == "answer":
            final = plan.get("final", "").strip()
            memory.add({"step": step, "final": final})
            return final


        if action == "tool":
            name = plan.get("name")
            tool_input = plan.get("input") or {}
            # To prevent from repeating same step
            key = hashlib.md5(json.dumps(plan, sort_keys=True).encode()).hexdigest()
            if key in seen_actions:
                return f"Stopped: repeated action at step {step}."
            seen_actions.add(key)

            if name not in TOOLS:
                return f"ToolError: unknown tool '{name}'."

            try:
                result = TOOLS[name].fn(**tool_input)
            except TypeError as e:
                result = f"ToolInputError: {e}"
            except Exception as e:
                result = f"ToolError: {e}"

            messages += [
                {"role":"assistant","content": json.dumps(plan, ensure_ascii=False)},
                {"role":"tool","content": f"{name} -> {result}"},
            ]
            memory.add({"step": step, "tool": name, "result": result})
            continue

        return f"PlannerError: unsupported action at step {step}: {plan}"
    return "Error: Max steps reached."

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True, help="What should the agent do?")
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()

    config = yaml.safe_load(open(args.config))
    reponse = run_agent(args.goal, config)
    print(reponse)
    sys.exit(0 if "error" not in reponse.lower() else 1)
