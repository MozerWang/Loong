import json
import random
import os
from utils.args import parse_arguments
from utils.config import load
from utils.generate import generate
from utils.util import create_path, continue_gen


if __name__ == '__main__':
    args = parse_arguments()
    random.seed(args.seed)

    config = load(open(f"{args.model_config_dir}/{args.models}"))
    tag = "generate_response"

    with open(args.output_process_path, "r") as f:
        generate_data = [json.loads(item.strip()) for item in f.readlines()]

    if not os.path.exists(args.output_path):
        create_path(args.output_path)
        # api
        generate(generate_data, config, args.output_path, args.process_num_gen, tag=tag)
    else:

        if args.continue_gen:
            continue_generate_data = continue_gen(args.output_path, generate_data, tag=tag)
            # api
            generate(continue_generate_data, config, args.output_path, args.process_num_gen, tag=tag)
        else:
            print(f"Path exist: {args.output_path}")
