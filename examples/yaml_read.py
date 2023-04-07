#!/usr/bin/env python
# Script to Read the values of a yaml file, not moving forward w for data gen since low-level for query gen

import yaml

# As per- https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
with open("./openapi/specs/google-calendar.yaml", "r") as stream:
    try:
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


print(type(data))
print(data.keys())
