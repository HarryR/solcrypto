#!/usr/bin/env python
import json
import sys


if __name__ == "__main__":
    file_path, dep_name = sys.argv[1:]
    with open(file_path, 'r') as handle:
        data = json.load(handle)
        version = data['dependencies'][dep_name]
        print(version[1:])

