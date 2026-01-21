#!/usr/bin/env python3
import argparse
import sys

try:
    from . import info
except ImportError:  # Allows running as a script from within the package dir.
    sys.path.insert(0, "..")
    from wik import info


def _build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="Search any topic")
    parser.add_argument("-i", "--info", help="Get info on any topic")
    parser.add_argument("-q", "--quick", help="Get the summary on any topic")
    parser.add_argument(
        "-l",
        "--lang",
        help="Get info in your native language (default english)",
        default="en",
    )
    parser.add_argument(
        "-x", "--rand", help="Get random Wikipedia article", action="store_true"
    )
    parser.add_argument(
        "--no-cache",
        help="Disable on-disk cache for this run",
        action="store_true",
    )
    parser.add_argument(
        "--clear-cache",
        help="Clear cached pages and exit",
        action="store_true",
    )
    return parser


def arguments(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)
    args.lang = args.lang.lower()

    if args.no_cache:
        info.set_cache_enabled(False)
    if args.clear_cache:
        removed = info.clear_cache()
        print(f"Cleared {removed} cached page(s).")
        return

    if not any([args.quick, args.info, args.search, args.rand]):
        parser.print_help()
        return

    if args.quick:
        info.getSummary(args.quick, args.lang)
    if args.info:
        info.getInfo(args.info, args.lang)
    if args.search:
        info.searchInfo(args.search, args.lang)
    if args.rand:
        info.getRand(args.lang)


if __name__ == "__main__":
    arguments()
