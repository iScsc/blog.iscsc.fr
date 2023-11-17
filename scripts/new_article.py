import sys
import re
import requests
import yaml

for file_path in sys.argv[1:]:
    # Check that this is an article file
    if re.match("^src/content/posts/.+\.md$", file_path):
        # Read YAML Header
        with open(file_path, "r") as f:
            raw_txt = f.read()
            data = yaml.safe_load(raw_txt.split("---")[1])

        # Get rid of python objects, only keep basic types
        for key in data:
            if type(data[key]) not in [int, str, float, bool]:
                data[key] = str(data[key])

        # Add URL info
        file_name = file_path.split("/")[-1][:-3]
        data["url"] = f"https://iscsc.fr/posts/{file_name}"

        # Finally send Data
        requests.post("http://iscsc.fr:8001/new-blog", json=data)
        print(file_path, file_name, data)
