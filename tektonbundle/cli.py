"""Tekton Bundlelizer"""
import argparse
import glob
import os
import sys

from tektonbundle import tektonbundle


def main():
    """Console script for tektonbundle."""
    parser = argparse.ArgumentParser()
    parser.add_argument('directory',
                        help="Directory where to get all the yaml files.")
    parser.add_argument('parameters',
                        nargs='*',
                        help="Add parameters to pass to templates.")
    parser.add_argument('--skip-inlining',
                        help="Skip inlining these tasks, you can add many of "
                        "them separated by a comma.")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        raise Exception(f"{args.directory} should have been a directory")
    yaml_files = glob.glob(os.path.join(args.directory, "*.y*ml"))
    parameters = {i.split("=")[0]: i.split("=")[1] for i in args.parameters}
    skip_inlining = args.skip_inlining.split(",")
    print(
        tektonbundle.parse(yaml_files,
                           parameters=parameters,
                           skip_inlining=skip_inlining))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
