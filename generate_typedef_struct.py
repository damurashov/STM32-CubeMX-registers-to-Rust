import re
import sys
from command import command_output

RE_IDENTIFIER = r"\b([a-zA-Z_][a-zA-Z0-9_]+)"

def process_typedef_struct(typedef):
    print(typedef)


def iter_typedef_struct(text):
    re_preamble = r"typedef\s+struct.*\n"
    re_body = r"{((?:[^\}]+\n)+)\}\s?"
    re_typedef_name = r'(' + RE_IDENTIFIER + r')' + r";"
    re_complete = re_preamble + re_body + re_typedef_name

    re_compiled = re.compile(re_complete, re.MULTILINE)

    for m in re_compiled.finditer(text):
        yield(m)


def body_line_iter_identifiers(body_line):
    re_int = r"u?int([0-9]+)_t"
    re_complete = re_int + r'\s' + RE_IDENTIFIER

    for m in re.compile(re_complete).finditer(body_line):
        yield m


def body_get_body_lines(body):
    body = body.replace('\r', '')
    body = body.split('\n')

    return body


def body_lines_test_print_identifiers(body_lines):
    for body_line in body_lines:
        for match in body_line_iter_identifiers(body_line):
            print(match)
            print(match.group(1))
            print(match.group(2))


def identifier_get_register_name(identifier):
    return identifier.replace('_TypeDef', '')


if __name__ == "__main__":
    text = command_output(f"cat {sys.argv[1]}")

    for t in iter_typedef_struct(text):
        body = t.group(1)
        body = body_get_body_lines(body)
        body_lines_test_print_identifiers(body)
        identifier = t.group(2)
        identifier = identifier_get_register_name(identifier)
        # print(body)
        # print(identifier)
        # begin = t.span()[0]
        # end = t.span()[1]
        # print(text[begin:end])
