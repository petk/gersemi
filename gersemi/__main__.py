import argparse
from dataclasses import fields
import pathlib
import sys
from lark import __version__ as lark_version
from gersemi.configuration import (
    make_configuration,
    make_default_configuration_file,
    Configuration,
    ListExpansion,
    indent_type,
    workers_type,
)
from gersemi.mode import get_mode
from gersemi.return_codes import SUCCESS, FAIL
from gersemi.runner import run, print_to_stderr
from gersemi.__version__ import __title__, __version__


class GenerateConfigurationFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(make_default_configuration_file())


class ShowVersion(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(f"{__title__} {__version__}")
        print(f"lark {lark_version}")
        print(f"Python {sys.version}")


class ToggleAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(
            namespace,
            self.dest,
            not option_string.startswith("--no-"),
        )


def create_argparser():
    parser = argparse.ArgumentParser(
        description="A formatter to make your CMake code the real treasure.",
        prog="gersemi",
        add_help=False,
    )
    modes_group = parser.add_argument_group("modes")
    modes_group.add_argument(
        "-c",
        "--check",
        dest="check_formatting",
        action="store_true",
        help=f"""
    Check if files require reformatting.
    Return {SUCCESS} when there's nothing to reformat.
    Return {FAIL} when some files would be reformatted.
            """,
    )
    modes_group.add_argument(
        "-i",
        "--in-place",
        dest="in_place",
        action="store_true",
        help="Format files in-place.",
    )
    modes_group.add_argument(
        "--diff",
        dest="show_diff",
        action="store_true",
        help="Show diff on stdout for each formatted file instead.",
    )
    modes_group.add_argument(
        "--default-config",
        nargs=0,
        action=GenerateConfigurationFile,
        help="Generate default .gersemirc configuration file.",
    )
    modes_group.add_argument(
        "--version",
        nargs=0,
        dest="show_version",
        action=ShowVersion,
        help="Show version.",
    )
    modes_group.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )

    conf_doc: dict[str, str] = {
        item.name: item.metadata["description"] for item in fields(Configuration)
    }

    configuration_group = parser.add_argument_group(
        title="configuration", description=Configuration.__doc__
    )
    configuration_group.add_argument(
        "-l",
        "--line-length",
        metavar="INTEGER",
        dest="line_length",
        type=int,
        help=f"{conf_doc['line_length']} [default: {Configuration.line_length}]",
    )
    configuration_group.add_argument(
        "--indent",
        metavar="(INTEGER | tabs)",
        dest="indent",
        type=indent_type,
        help=f"{conf_doc['indent']} [default: {repr(Configuration.indent)}]",
    )
    configuration_group.add_argument(
        "--unsafe",
        dest="unsafe",
        action="store_true",
        help=conf_doc["unsafe"],
    )
    configuration_group.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help=conf_doc["quiet"],
    )
    configuration_group.add_argument(
        "--color",
        dest="color",
        action="store_true",
        help=conf_doc["color"],
    )
    configuration_group.add_argument(
        "--definitions",
        dest="definitions",
        metavar="src",
        default=None,
        nargs="+",
        type=pathlib.Path,
        help=conf_doc["definitions"],
    )
    configuration_group.add_argument(
        "--list-expansion",
        dest="list_expansion",
        choices=["favour-inlining", "favour-expansion"],
        help=f"""
    {conf_doc['list_expansion']}
    {" ".join(map(lambda attr: attr.description, ListExpansion))}
    [default: {Configuration.list_expansion.value}]
            """,
    )
    configuration_group.add_argument(
        "-w",
        "--workers",
        metavar="(INTEGER | max)",
        dest="workers",
        type=workers_type,
        help=f"""
    {conf_doc['workers']} [default: {repr(Configuration.workers)}]
        """,
    )
    configuration_group.add_argument(
        "--cache",
        "--no-cache",
        dest="cache",
        action=ToggleAction,
        nargs=0,
        default=None,
        help=f"""
    {conf_doc["cache"]}
    [default: cache enabled]
        """,
    )
    configuration_group.add_argument(
        "--warn-about-unknown-commands",
        "--no-warn-about-unknown-commands",
        dest="warn_about_unknown_commands",
        action=ToggleAction,
        nargs=0,
        default=None,
        help=f"""
    {conf_doc["warn_about_unknown_commands"]}
    [default: warnings enabled]
        """,
    )

    parser.add_argument(
        dest="sources",
        metavar="src",
        nargs="*",
        type=pathlib.Path,
        help="""
    File or directory to format.
    If only `-` is provided, input is taken from stdin instead.
            """,
    )

    return parser


def is_stdin_mixed_with_file_input(sources):
    if sources is None:
        return False

    return pathlib.Path("-") in sources and len(sources) != 1


def postprocess_args(args):
    args.sources = set(args.sources)
    if args.definitions is not None:
        args.definitions = set(args.definitions)


def main():
    argparser = create_argparser()
    args = argparser.parse_args()
    postprocess_args(args)

    if any(map(is_stdin_mixed_with_file_input, [args.sources, args.definitions])):
        print_to_stderr("Don't mix stdin with file input")
        sys.exit(FAIL)

    if len(args.sources) < 1:
        sys.exit(SUCCESS)

    try:
        configuration = make_configuration(args)
        mode = get_mode(args)
    except Exception as exception:  # pylint: disable=broad-except
        print_to_stderr(exception)
        sys.exit(FAIL)

    sys.exit(run(mode, configuration, args.sources))


if __name__ == "__main__":
    main()
