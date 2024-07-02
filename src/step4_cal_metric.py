from utils.args import parse_arguments
from utils.metric import cal_metric


if __name__ == '__main__':
    args = parse_arguments()

    print("------------------ All metrics: ------------------")
    cal_metric(args, tag="eval_response")

    for set in [1,2,3,4]:
        print(f"------------------ Set {set} metrics ------------------")
        for level in [1,2,3,4]:
            cal_metric(args, tag="eval_response", set=set, level=level)
        print("")