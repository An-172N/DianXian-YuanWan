# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import sys
import argparse
import random


def main():
    project = '点线 Project'
    title = '圆玩 ~ Oceanfront'
    version = '0.1'
    author = 'An_172N'
    sys.dont_write_bytecode = True
    sys.modules['numpy'] = None
    parser = argparse.ArgumentParser()
    for i, j in (('-s', 1), ('-l', 1), ('-sd', None)):
        parser.add_argument(i, type=int, default=j)
    args = parser.parse_args()
    args_tuple = (int(args.s), int(args.l))
    random.seed(args.sd)

    import pygame

    clock = pygame.time.Clock()
    pygame.display.init()
    pygame.display.set_caption(title)
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)

    import KERNEL

    print(f"{project} | {title} | Ver {version} | By {author}")
    KERNEL.update(clock, args_tuple, version, title)


if __name__ == "__main__":
    main()