import sys
import re

RE_IDENTIFIER = r"\b([a-zA-Z_][a-zA-Z0-9_]+)"

def filter_define(content):
   return list(filter(lambda s: '#define' in s, content))

def filter_is(content):
    return list(filter(lambda s: 'IS_' not in s, content))

def filter_typedef(content):
    return list(filter(lambda s: 'TypeDef' not in s, content))

def filter_private(content):
    return list(filter(lambda s: "__" not in s, content))

def replace_comments(content):
    content = [c.replace('/*', '//') for c in content]
    content = [c.replace('*/', '') for c in content]
    content = [c.strip() for c in content]

    return content

def replace_string_literals(content):
    def repl(ln):
        return re.sub(r"\b((?:0x)?[0-9ABCDEF]+)UL?", r"\1u32", ln)

    return [repl(c) for c in content]


def replace_excessive_space(content):
    def repl(ln):
        return re.sub("\s+", ' ', ln)

    return [repl(c) for c in content]


def replace_define(content):
    def repl(ln):
        return re.sub(r"#define\s+", "", ln)

    return [repl(c) for c in content]


def parse_values(content):
    def repl(ln):
        # return re.sub(r"^#define\s+([^\s])\s(.*)\/\/.*$", r"const unsigned \1 = \2", ln)
        # return re.sub(r"([^\s]+)\s([^\/]+)(.*)", r"unsigned \1 = \2; \3", ln)
        m = re.search(r"([^\s]+)\s([^\/]+)(.*)", ln)
        return [c.strip() for c in m.groups()]

    return [repl(c) for c in content]


def filter_missing_values(content):
    identifiers = set(c[0] for c in content)
    res = []

    for c in content:
        mentioned = re.search(RE_IDENTIFIER, c[1])

        if mentioned is not None:
            if not all([ref in identifiers for ref in mentioned.groups()]):
                continue

        res.append(c)

    return res


def generate_c_code(content):
    return [f"unsigned {c[0]} = {c[1]}; {c[2]}" for c in content]


def generate_rust_code(content):
    return [f"const {c[0]}: u32 = {c[1]};" for c in content]


def transform_identifiers_upper(values):
    res = []

    for v in values:
        v[0] = v[0].upper()

        for ident in re.compile(RE_IDENTIFIER).finditer(v[1]):
            span = ident.span()
            fragment = v[1][span[0]:span[1]]
            v[1] = v[1].replace(fragment, fragment.upper())

        res.append(v)

    return res


if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as f:
        content = f.read()
        content = content.split(b'\r\n')
        content = [c.split(b'\n') for c in content]
        content = [c[0] for c in content]
        content = [c.decode('cp1251') for c in content]

    content = filter_define(content)
    content = filter_is(content)
    content = filter_typedef(content)
    content = filter_private(content)
    content = replace_comments(content)
    content = replace_string_literals(content)  # Should be replaced w/ u32 suffix for rust code generation
    content = replace_excessive_space(content)
    content = replace_define(content)
    content = parse_values(content)
    content = filter_missing_values(content)
    content = transform_identifiers_upper(content)

    # print('\n'.join(generate_c_code(content)))
    print('\n'.join(generate_rust_code(content)))
