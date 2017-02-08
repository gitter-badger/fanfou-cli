import argparse
import logging
from .fan import Fan


def parse_args():
    parser = argparse.ArgumentParser()
    # nargs参数的妙用
    # add参数是可选的，但是我也想不加-a时且没有其他参数时也执行这个动作
    # 或者一个nagrs=*的positional，但是也可以不提供
    parser.add_argument('-n', '--new', metavar='X', nargs='*', help='发布新的状态')
    parser.add_argument('-r', '--revert', action='store_true', help='撤回前一条消息')
    parser.add_argument('-s', '--save_all_statuses', action='store_true', help='备份所有状态')
    parser.add_argument('-p', '--protect', metavar='0/1', type=int, help='需要我批准才能查看我的消息')
    parser.add_argument('-m', '--me', action='store_true', help='查看个人信息')
    parser.add_argument('-l', '--view', action='store_true', help='浏览模式')
    parser.add_argument('-d', '--random', action='store_true', help='随便看看')
    parser.add_argument('-v', '--verbose', action='count', default=0)
    return parser.parse_known_args()


def open_fanfou():
    import webbrowser
    webbrowser.open_new_tab('http://fanfou.com')


def main():
    fan = Fan()
    args, unknown = parse_args()

    level = logging.DEBUG if args.verbose >= 2 else logging.INFO
    logging.basicConfig(level=level,
                        format='%(asctime)s [%(module)14s] [line:%(lineno)4d] [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    if args.save_all_statuses:
        fan.save_all_statuses()
    elif args.revert:
        fan.revert()
    elif args.protect is not None:
        fan.api.protect(bool(args.protect))
    elif args.me:
        print(fan.me())
    elif args.view:
        fan.view()
    elif args.random:
        fan.random_view()
    else:
        if args.new:
            status = ' '.join(args.new)
        elif unknown:
            status = ' '.join(unknown)
        else:
            open_fanfou()
            return
        fan.update_status(status)


if __name__ == '__main__':
    main()
