import json


def write_jsonl_lines(path, file):
    with open(path, 'w') as outfile:
        for entry in file:
            json.dump(entry, outfile)
            outfile.write('\n')


def read_jsonl_lines(input_path):
    with open(input_path) as f:
        lines = f.readlines()
        return [json.loads(l.strip()) for l in lines]