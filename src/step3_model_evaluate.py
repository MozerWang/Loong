import os
from utils.args import parse_arguments
from utils.prompt import get_evaluate_prompts
from utils.generate import generate
from utils.util import create_path
from utils.config import load


if __name__ == '__main__':
    args = parse_arguments()

    eval_config = load(open(f"{args.model_config_dir}/{args.eval_model}"))

    if not os.path.exists(args.evaluate_output_path):
        create_path(args.evaluate_output_path)
        evaluate_prompts = get_evaluate_prompts(args, tag="generate_response")
        generate(evaluate_prompts, eval_config, args.evaluate_output_path, args.process_num, tag="eval_response")
    else:
        print(f"Path exist: {args.evaluate_output_path}")
