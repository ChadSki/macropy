from macropy.core.macros import *
from macropy.core import *
macros = Macros()

def u(tree):
    """Stub to make the IDE happy"""

def name(tree):
    """Stub to make the IDE happy"""


@Walker
def _unquote_search(tree):
    if isinstance(tree, BinOp) and type(tree.left) is Name and type(tree.op) is Mod:
        if 'u' == tree.left.id:
            return Literal(Call(Name(id="ast_repr"), [tree.right], [], None, None))
        elif 'name' == tree.left.id:
            return Literal(Call(Name(id="Name"), [], [keyword("id", tree.right)], None, None))
        elif 'ast' == tree.left.id:
            return Literal(tree.right)
        elif 'ast_list' == tree.left.id:
            return Literal(Call(Name(id="List"), [], [keyword("elts", tree.right)], None, None))


@macros.expr()
def q(tree):
    tree = _unquote_search.recurse(tree)
    return ast_repr(tree)


@macros.block()
def q(tree):
    body = _unquote_search.recurse(tree.body)
    return Assign([Name(id=tree.items[0].optional_vars.id)], ast_repr(body))
