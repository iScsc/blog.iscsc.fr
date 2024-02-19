import os
import sys
import re
import requests
import yaml

for file_path in sys.argv[1:]:
    # Check that this is an article file
    if re.match("^src/content/posts/.+\.md$", file_path):
        ## Read YAML Header
        with open(file_path, "r") as f:
            raw_txt = f.read()
            data = yaml.safe_load(raw_txt.split("---")[1])

        ## Get rid of python objects, only keep basic types
        for key in data:
            if type(data[key]) not in [int, str, float, bool]:
                data[key] = str(data[key])

        ## Add URL info:
        # we have to deal with both possibilities of new article:
        # - an article as a .md file which URL is the name
        # - a leaf bundle article (https://gohugo.io/content-management/page-bundles/#leaf-bundles):
        #   it's an article which name is the folder's name and body is in a index.md in this directory
        dirname, basename = os.path.split(file_path)
        if basename == "index.md":
            # leaf bundle: name is directory name
            file_name = os.path.basename(dirname)
        else:
            # direct article file: name is file name
            file_name = basename[:-3] # get rid of the `.md`

        data["url"] = f"https://iscsc.fr/posts/{file_name}"

        ## Finally send Data
        requests.post("http://iscsc.fr:8001/new-blog", json=data)
        print(file_path, file_name, data)
