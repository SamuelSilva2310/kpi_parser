import json

FILENAME = "full_config.fe1.json"
with open(FILENAME, "r+") as f:
    with open('test.json', 'w') as w:
        run = True
        i=2048
        lines = f.readlines(i)
        while len(lines) > 0:
            for line in lines:
                if not line.strip().startswith("/"):
                    if "/*" in line or "*/" in line:
                        line = line.replace("/*", "")
                    w.write(line)
                else:
                    print("[LINE]", line)
            lines = f.readlines(i)