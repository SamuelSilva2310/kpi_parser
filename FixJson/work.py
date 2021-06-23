import json
import re
import ast
i = 0
with open("../parsed.json", "r") as f:
    s = f.read()
    data = ast.literal_eval(s)

print(type(json.loads(json.dumps(data))))

