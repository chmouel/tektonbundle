"""Tekton Bundlelizer"""
import argparse
import glob
import os
import sys

from tektonbundle import tektonbundle


def bundler(arguments):
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
    parser.add_argument(
        "--only-bundled",
        default=False,
        action="store_true",
        help=
        "Print only the files that have been bundled (tekton files) and skip others."
    )
    args = parser.parse_args(arguments)

    yaml_files = []
    for file_or_dir in args.files:
        if os.path.isdir(file_or_dir):
            yaml_files = yaml_files + glob.glob(
                os.path.join(file_or_dir, "*.y*ml"))
        else:
            yaml_files.append(file_or_dir)

    parameters = {i.split("=")[0]: i.split("=")[1] for i in args.parameters}
    skip_inlining = args.skip_inlining.split(",") if args.skip_inlining else []
    parsed = tektonbundle.parse(yaml_files,
                                parameters=parameters,
                                skip_inlining=skip_inlining)
    ret = ["--- "]
    ret.append(parsed['bundle'])
    if not args.only_bundled:
        ret.append("--- ")
        ret.append("\n--- \n".join(parsed['ignored_not_tekton'] +
                                   parsed['ignored_not_k8']))
    return ret


def main():
    print("\n".join(bundler(sys.argv[1:])))


if __name__ == "__main__":
    sys.exit(main())  # pragma: no-cover
