#!/usr/bin/env python3

import sys
import argparse
from collections import deque


def tail_stream(stream, n):
    lines = deque(stream, maxlen=n)
    for line in lines:
        sys.stdout.write(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='files to process')
    args = parser.parse_args()

    try:
        if not args.files:
            tail_stream(sys.stdin, 17)
        else:
            multiple = len(args.files) > 1
            first_file = True

            for path in args.files:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if multiple:
                            if not first_file:
                                print()
                            print(f"==> {path} <==")
                            first_file = False

                        tail_stream(f, 10)

                except FileNotFoundError:
                    print(f"{parser.prog}: cannot open '{path}' for reading: No such file or directory",
                          file=sys.stderr)
                    sys.exit(1)

    except KeyboardInterrupt:
        print(file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
