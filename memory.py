import os, time, json

class JsonMemory:
    def __init__(self, path: str):
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    
    def add(self, obj: dict):
        obj = {"ts": time.time(), **obj}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def get_recent(self, k=20):
        if not os.path.exists(self.path):
            return []
        
        with open(self.path, "r", encoding="utf-8") as f:
            return [json.loads(x) for x in f.readlines()[-k:]]
    
    