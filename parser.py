import time

FILENAME = "full_config.fe1.json"


def remove_comments():
    with open(FILENAME, "r+") as f:
        with open('parsed.json', 'w') as w:
            run = True
            i = 2048
            lines = f.readlines(i)
            multiline_comment = False
            while len(lines) > 0:
                for line in lines:
                    if not line.strip().startswith("//"):

                        if multiline_comment and "*/" not in line:
                            continue

                        if "*/" in line and multiline_comment:
                            multiline_comment = False
                            continue

                        if "/*" in line and "*/" not in line:
                            multiline_comment = True
                            continue

                        if "//" in line and "://" not in line:
                            line = line.split("//")[0]

                        if "/*" in line:
                            line = line.split("/*")[0]

                        if "*/" in line:
                            line = line.replace("*/", "")

                        if "true" in line:
                            line = line.replace("true", "True")
                        elif "false" in line:
                            line = line.replace("false", "False")

                        w.write(line)

                lines = f.readlines(i)


remove_comments()
