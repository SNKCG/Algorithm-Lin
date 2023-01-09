import sys
if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import time
from model import *
from tools import *
from evaluation_tools import evaluate
import gym

def main(args):
    custom = input('Please input the evaluate name\n')
    timeStr = custom + '-' + time.strftime('%Y.%m.%d-%H-%M-%S', time.localtime(time.time()))

    if args.no_cuda:
        device = torch.device('cpu')
    else:
        device = torch.device('cuda', args.device)
        torch.cuda.set_device(args.device)

    torch.cuda.set_device(args.device)
    torch.set_num_threads(1)
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)

    # 创建非并行环境
    envs = gym.make(args.id,
                    setting = args.setting,
                    container_size=args.container_size,
                    item_set=args.item_size_set,
                    data_name=args.dataset_path,
                    load_test_data = args.load_dataset,
                    internal_node_holder=args.internal_node_holder,
                    leaf_node_holder=args.leaf_node_holder,
                    LNES = args.lnes,
                    shuffle=args.shuffle)

    PCT_policy =  DRL_GAT(args)
    PCT_policy =  PCT_policy.to(device)

    if args.load_model:
        PCT_policy = load_policy(args.model_path, PCT_policy)
        print('Pre-train model loaded!', args.model_path)

    backup(timeStr, args, None)
    
    # 进行evaluation
    evaluate(PCT_policy, envs, timeStr, args, device,
             eval_freq=args.evaluation_episodes, factor=args.normFactor)

if __name__ == '__main__':
    registration_envs()
    args = get_args()
    main(args)