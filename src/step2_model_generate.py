import json
import random
import os
from utils.args import parse_arguments
from utils.config import load
from utils.generate import generate
from utils.util import create_path


if __name__ == '__main__':
    args = parse_arguments()
    random.seed(args.seed)

    config = load(open(f"{args.model_config_dir}/{args.models}"))

    if not os.path.exists(args.output_path):
        create_path(args.output_path)
        with open(args.output_process_path, "r") as f:
            generate_data = [json.loads(item.strip()) for item in f.readlines()]
        # api
        generate(generate_data, config, args.output_path, args.process_num, tag="generate_response")
    else:
        print(f"Path exist: {args.output_path}")
