from lark import Discard
from lark.visitors import Transformer


def drop_comments_and_whitespaces(tree):
    class Impl(Transformer):  # pylint: disable=too-few-public-methods
        def _drop_node(self, _):
            raise Discard()

        leading_space = _drop_node
        trailing_space = _drop_node
        non_command_element = _drop_node
        line_comment = _drop_node
        bracket_comment = _drop_node
        SPACE = _drop_node
        NEWLINE = _drop_node

    return Impl(visit_tokens=True).transform(tree)


def check_abstract_syntax_trees_equivalence(lhs, rhs):
    preprocess = drop_comments_and_whitespaces
    assert preprocess(lhs) == preprocess(rhs), "ASTs mismatch"


def check_code_equivalence(parser, lhs, rhs):
    lhs_parsed, rhs_parsed = parser.parse(lhs), parser.parse(rhs)
    check_abstract_syntax_trees_equivalence(lhs_parsed, rhs_parsed)
