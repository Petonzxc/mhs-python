#!/usr/bin/env python3

import sys
import argparse


def wc_bytes(data: bytes):
    lines = data.count(b'\n')
    words = len(data.split())
    bytes_count = len(data)
    return lines, words, bytes_count


def print_stats(lines, words, bytes_count, name=None):
    if name is None:
        print(f"{lines:7d} {words:7d} {bytes_count:7d}")
    else:
        print(f"{lines:7d} {words:7d} {bytes_count:7d} {name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='files to process')
    args = parser.parse_args()

    try:
        if not args.files:
            data = sys.stdin.buffer.read()
            lines, words, bytes_count = wc_bytes(data)
            print_stats(lines, words, bytes_count)
            return

        total_lines = 0
        total_words = 0
        total_bytes = 0
        multiple = len(args.files) > 1

        for path in args.files:
            try:
                with open(path, 'rb') as f:
                    data = f.read()
            except FileNotFoundError:
                print(f"wc.py: {path}: No such file or directory", file=sys.stderr)
                sys.exit(1)

            lines, words, bytes_count = wc_bytes(data)
            print_stats(lines, words, bytes_count, path)

            if multiple:
                total_lines += lines
                total_words += words
                total_bytes += bytes_count

        if multiple:
            print_stats(total_lines, total_words, total_bytes, "total")

    except KeyboardInterrupt:
        print(file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
