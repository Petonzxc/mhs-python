#!/usr/bin/env python3

import sys
import argparse


def number_lines(input_stream):
    line_number = 1
    for line in input_stream:
        print(f"{line_number:6}\t{line}", end='')
        line_number += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()
    
    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                number_lines(f)
        else:
            number_lines(sys.stdin)
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()