import re, json
import numpy as np


def extract_number(text):
    match = re.search(r'\[\[([0-9]*\.?[0-9]+)\]\]', text)
    if match:
        return float(match.group(1))
    match = re.search(r'\[([0-9]*\.?[0-9]+)\]', text)
    if match:
        return float(match.group(1))
    return None


def failure_prompts(args, tag):
    eval_lines = open(args.old_evaluate_output_path).readlines()
    gen_lines = open(args.old_output_path).readlines()
    scores = []
    effective_samples = []
    no_effective_samples = []
    for line in eval_lines:
        line = json.loads(line.strip())
        if not extract_number(line[tag]) or line['generate_response'] == "":
            no_effective_samples.append(line['id'])
    for line in gen_lines:
        line = json.loads(line.strip())
        if line['id'] in no_effective_samples:
            effective_samples.append(
                {'id': line['id'], 'prompt': line['prompt'], 'question': line['question'], 'answer': line['answer']})
    return effective_samples


def cal_metric(args, tag, level=None, set=None):
    lines = open(args.evaluate_output_path).readlines()
    scores = []
    effective_samples = []
    no_effective_samples = []
    for line in lines:
        line = json.loads(line.strip())

        _level = line.get("level", None)
        _set = line.get("set", None)
        if level and _level and _level != level:
            continue
        if set and _set and _set != set:
            continue

        if extract_number(line[tag]) is not None:
            scores.append(extract_number(line[tag]))
            effective_samples.append(line)
        else:
            no_effective_samples.append(line['id'])

    num_full_marks = sum(1 for x in scores if x == 100)
    # if no effective samples, then the metric is (0.0, 0.0, "0/0", 0.0)
    if len(effective_samples) == 0:
        scoring_success_rate = 0.0
        avg_score = 0.0
        perfect_rate_calculation = "0/0"
        perfect_rate = 0.0
    else:
        scoring_success_rate = len(effective_samples) / len(lines)
        avg_score = np.mean(scores)
        perfect_rate_calculation = f"{num_full_marks}/{len(effective_samples)}"
        perfect_rate = num_full_marks / len(effective_samples)
    
    metric = (scoring_success_rate, avg_score, perfect_rate_calculation, perfect_rate)

    print(f"level: {level}, set: {set}, scoring_success_rate: {metric[0]:.2f} , avg_score: {metric[1]:.2f} , perfect_rate_calculation: {metric[2]} , perfect_rate: {metric[3]:.2f}")
    return metric
