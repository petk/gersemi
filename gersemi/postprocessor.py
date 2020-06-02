from itertools import dropwhile
from typing import Iterator
from lark import Discard, Tree
from lark.tree import Meta
from lark.visitors import (
    Transformer,
    TransformerChain,
    Transformer_InPlace,
    v_args,
)
from gersemi.ast_helpers import is_newline, is_argument, is_comment
from gersemi.types import Node, Nodes
from gersemi.utils import pop_all


class RemoveSuperfluousEmptyLines(Transformer_InPlace):
    def _filter_superfluous_empty_lines(self, children) -> Iterator:
        consecutive_newlines = 0
        for child in children:
            if is_newline(child):
                if consecutive_newlines >= 2:
                    continue
                consecutive_newlines += 1
            else:
                consecutive_newlines = 0
            yield child

    def _drop_edge_empty_lines(self, children) -> Iterator:
        while len(children) > 0 and is_newline(children[-1]):
            children.pop()
        return dropwhile(is_newline, children)

    def _make_node(self, node_type, children) -> Tree:
        new_children = self._filter_superfluous_empty_lines(
            self._drop_edge_empty_lines(children)
        )
        return Tree(node_type, list(new_children))

    def file(self, children) -> Tree:
        return self._make_node("file", children)

    def block_body(self, children) -> Tree:
        return self._make_node("block_body", children)


class IsolateCommentedArguments(Transformer_InPlace):
    def arguments(self, children) -> Tree:
        new_children: Nodes = []
        accumulator: Nodes = []
        for child in children:
            if is_argument(child):
                new_children += pop_all(accumulator)

            accumulator += [child]
            if is_comment(child) and is_argument(accumulator[0]):
                new_children += [Tree("commented_argument", pop_all(accumulator))]
            if is_newline(child):
                new_children += pop_all(accumulator)
        new_children += accumulator
        return Tree("arguments", new_children)


class SimplifyParseTree(Transformer_InPlace):
    @v_args(meta=True)
    def non_command_element(self, children: Nodes, meta: Meta) -> Tree:
        if len(children) == 0:
            raise Discard
        return Tree("non_command_element", children, meta)

    def arguments(self, children: Nodes) -> Tree:
        return Tree("arguments", [child for child in children if not is_newline(child)])

    def argument(self, children: Nodes) -> Node:
        return children[0]


class PreserveCustomCommandFormatting(Transformer_InPlace):
    builtin_commands = {
        "break",
        "cmake_host_system_information",
        "cmake_minimum_required",
        "cmake_parse_arguments",
        "cmake_policy",
        "configure_file",
        "continue",
        "else",
        "elseif",
        "endforeach",
        "endfunction",
        "endif",
        "endmacro",
        "endwhile",
        "execute_process",
        "file",
        "find_file",
        "find_library",
        "find_package",
        "find_path",
        "find_program",
        "foreach",
        "function",
        "get_cmake_property",
        "get_directory_property",
        "get_filename_component",
        "get_property",
        "if",
        "include",
        "include_guard",
        "list",
        "macro",
        "mark_as_advanced",
        "math",
        "message",
        "option",
        "return",
        "separate_arguments",
        "set",
        "set_directory_properties",
        "set_property",
        "site_name",
        "string",
        "unset",
        "variable_watch",
        "while",
        "add_compile_definitions",
        "add_compile_options",
        "add_custom_command",
        "add_custom_target",
        "add_definitions",
        "add_dependencies",
        "add_executable",
        "add_library",
        "add_link_options",
        "add_subdirectory",
        "add_test",
        "aux_source_directory",
        "build_command",
        "create_test_sourcelist",
        "define_property",
        "enable_language",
        "enable_testing",
        "export",
        "fltk_wrap_ui",
        "get_source_file_property",
        "get_target_property",
        "get_test_property",
        "include_directories",
        "include_external_msproject",
        "include_regular_expression",
        "install",
        "link_directories",
        "link_libraries",
        "load_cache",
        "project",
        "remove_definitions",
        "set_source_files_properties",
        "set_target_properties",
        "set_tests_properties",
        "source_group",
        "target_compile_definitions",
        "target_compile_features",
        "target_compile_options",
        "target_include_directories",
        "target_link_directories",
        "target_link_libraries",
        "target_link_options",
        "target_precompile_headers",
        "target_sources",
        "try_compile",
        "try_run",
        "ctest_build",
        "ctest_configure",
        "ctest_coverage",
        "ctest_empty_binary_directory",
        "ctest_memcheck",
        "ctest_read_custom_files",
        "ctest_run_script",
        "ctest_sleep",
        "ctest_start",
        "ctest_submit",
        "ctest_test",
        "ctest_update",
        "ctest_upload",
        "build_name",
        "exec_program",
        "export_library_dependencies",
        "install_files",
        "install_programs",
        "install_targets",
        "load_command",
        "make_directory",
        "output_required_files",
        "qt_wrap_cpp",
        "qt_wrap_ui",
        "remove",
        "subdir_depends",
        "subdirs",
        "use_mangled_mesa",
        "utility_source",
        "variable_requires",
        "write_file",
    }

    def __init__(self, code):
        super().__init__()
        self.code = code

    def _get_original_formatting(self, arguments):
        if len(arguments.children) == 0:
            content = ""
        else:
            start, end = arguments.meta.start_pos, arguments.meta.end_pos
            content = self.code[start:end]
        return Tree("formatted_node", [content])

    def _get_indentation(self, meta):
        end = meta.start_pos
        start = end - meta.column + 1
        return self.code[start:end]

    def _make_custom_command(self, children, meta, indentation):
        identifier, arguments = children
        return Tree(
            "custom_command",
            [
                indentation,
                identifier,
                arguments,
                self._get_original_formatting(arguments),
            ],
            meta,
        )

    def _is_builtin(self, command_invocation_children):
        identifier, *_ = command_invocation_children
        return identifier in self.builtin_commands

    @v_args(meta=True)
    def command_invocation(self, children, meta):
        if self._is_builtin(children):
            return Tree("command_invocation", children, meta)

        return self._make_custom_command(children, meta, self._get_indentation(meta))


def PostProcessor(code: str) -> Transformer:
    chain = TransformerChain(
        PreserveCustomCommandFormatting(code),
        IsolateCommentedArguments(),
        SimplifyParseTree(),
        RemoveSuperfluousEmptyLines(),
    )
    return chain
