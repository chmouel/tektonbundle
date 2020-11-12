"""Tekton Bundlelizer"""
import argparse
import glob
import os
import sys

from tektonbundle import tektonbundle


def main():
    """Console script for tektonbundle."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'files',
        nargs='+',
        help="Files and/or directories where to get all the yaml files.")
    parser.add_argument('parameters',
                        nargs='*',
                        help="Add parameters to pass to templates.")
    parser.add_argument('--skip-inlining',
                        help="Skip inlining these tasks, you can add many of "
                        "them separated by a comma.")
    parser.add_argument("--print-skipped",
                        default=False,
                        action="store_true",
                        help="Print non tekton files too.")
    args = parser.parse_args()

    yaml_files = []
    for file_or_dir in args.files:
        if os.path.isdir(file_or_dir):
            yaml_files = yaml_files + glob.glob(
                os.path.join(file_or_dir, "*.y*ml"))
        else:
            yaml_files.append(file_or_dir)

    parameters = {i.split("=")[0]: i.split("=")[1] for i in args.parameters}
    skip_inlining = args.skip_inlining.split(",") if args.skip_inlining else []
    ret = tektonbundle.parse(yaml_files,
                             parameters=parameters,
                             skip_inlining=skip_inlining)
    print("--- ")
    print(ret['bundle'])
    if args.print_skipped:
        print("--- ")
        print("\n--- \n".join(ret['ignored_not_tekton'] +
                              ret['ignored_not_k8']))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
