import os
import json


def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for _ in file)


def create_path(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def continue_gen(input_path, gen_data, tag):
    seen_id = dict()
    with open(input_path, 'r') as f:
        for item in f.readlines():
            js = json.loads(item.strip())
            if js[tag]:
                seen_id[js['id']] = js
    rewrite_data, continue_generate_data = [], []
    seen_rewrite = set()
    for item in gen_data:
        _id = item['id']
        if _id in seen_rewrite:
            continue
        if _id not in seen_id:
            continue_generate_data.append(item)
        else:
            rewrite_data.append(seen_id[_id])
        # dedup
        seen_rewrite.add(_id)
    with open(input_path, 'w') as f:
        for item in rewrite_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"continue_gen: input_path={input_path}, rewrite_data_num={len(rewrite_data)}, tag={tag}")
    return continue_generate_data
