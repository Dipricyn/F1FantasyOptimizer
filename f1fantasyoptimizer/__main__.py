#!/usr/bin/env python3
import argparse


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--gui", action='store_true')
    args = arg_parser.parse_args()
    if args.gui:
        import f1fantasyoptimizer.ui.gui as gui
        gui.main()
    else:
        import f1fantasyoptimizer.ui.cli as cli
        cli.main()


if __name__ == '__main__':
    main()
