import re
import sys
from command import command_output

RE_IDENTIFIER = r"\b([a-zA-Z_][a-zA-Z0-9_]+)"

def process_typedef_struct(typedef):
    print(typedef)


def text_iter_typedef_struct(text):
    re_preamble = r"typedef\s+struct.*\n"
    re_body = r"{((?:[^\}]+\n)+)\}\s?"
    re_typedef_name = r'(' + RE_IDENTIFIER + r')' + r";"
    re_complete = re_preamble + re_body + re_typedef_name

    re_compiled = re.compile(re_complete, re.MULTILINE)

    for m in re_compiled.finditer(text):
        yield(m)


def body_iter_identifiers(body):
    re_int = r"u?int([0-9]+)_t"
    re_complete = re_int + r'\s+' + RE_IDENTIFIER + r"[^\n]+\n"

    for m in re.compile(re_complete).finditer(body):
        yield m


def body_iter_offset_pair(body):
    """
    @yield (identifier, offset), ...
    """
    offset = 0x0

    for match in body_iter_identifiers(body):
        offset_inc = int(match.group(1))
        identifier = match.group(2)

        yield identifier, int(offset / 8)

        offset += offset_inc



def body_get_body_lines(body):
    body = body.replace('\r', '')
    body = body.split('\n')

    return body


def body_test_print_identifiers(body):
    for match in body_iter_identifiers(body):
        print(match)
        print(match.group(1))
        print(match.group(2))


def identifier_get_register_name(identifier):
    return identifier.replace('_TypeDef', '')


def ro_generate_rust_line(register, offset_pair):
    return f"pub const {register.upper()}_{offset_pair[0].upper()}_OFFSET: usize = {hex(offset_pair[1])};"


def ros_iter_rust_line(register, offset_pairs):
    for offset_pair in offset_pairs:
        yield ro_generate_rust_line(register, offset_pair)


def text_iter_rust_line(text):
    for t in text_iter_typedef_struct(text):
        identifier = t.group(2)
        register = identifier_get_register_name(identifier)
        body = t.group(1)

        for offset_pair in body_iter_offset_pair(body):
            yield ro_generate_rust_line(register, offset_pair)


def text_generate_rust_code(text):
    return list(text_iter_rust_line(text))


if __name__ == "__main__":
    text = command_output(f"cat {sys.argv[1]}")

    for rl in text_iter_rust_line(text):
        print(rl)
