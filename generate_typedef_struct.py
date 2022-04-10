import re
import sys
from command import command_output

RE_IDENTIFIER = r"\b([a-zA-Z_][a-zA-Z0-9_]+)"


def process_typedef_struct(typedef):
    print(typedef)


def iter_typedef_struct(text):
    re_preamble = r"typedef\s+struct.*\n"
    re_body = r"({(?:[^\}]+\n)+\}\s?)"
    re_typedef_name = r'(' + RE_IDENTIFIER + r')' + r";"
    re_complete = re_preamble + re_body + re_typedef_name

    re_compiled = re.compile(re_complete, re.MULTILINE)

    for m in re_compiled.finditer(text):
        yield(m)


def typedef_get_class(typedef):
    pass


if __name__ == "__main__":
    text = command_output(f"cat {sys.argv[1]}")

    for t in iter_typedef_struct(text):
        begin = t.span()[0]
        end = t.span()[1]
        print(text[begin:end])
