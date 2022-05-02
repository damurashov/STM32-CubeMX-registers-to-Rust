import sys
import re
from command import command_output

RE_IDENTIFIER = r"\b([a-zA-Z_][a-zA-Z0-9_]+)"
RE_IDENTIFIER_NOMATCH = r"\b[a-zA-Z_][a-zA-Z0-9_]+"
RE_SPACE = r"\s*"
RE_NUMERIC = r"\b((?:0x)?[0-9]+)\b"
RE_NUMERIC_NOMATCH = r"\b(?:0x)?[0-9]+\b"
RE_LINETERM = r"[^\n]+\n"

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
        return re.sub(r"\b((?:0x)?[0-9ABCDEF]+)UL?", r"\1usize", ln)

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
    return [f"pub const {c[0]}: usize = {c[1]};" for c in content]


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


def replace_redundant_parenthesis(values):
    for v in values:
        v[1] = v[1].strip()

        if '(' == v[1][0]:
            v[1] = v[1][1:]

        if ')' == v[1][-1]:
            v[1] = v[1][:-1]

    return values


def text_parse_braced_iter(defsuffix):
    defsuffix = defsuffix.strip()
    re_braced = r"^\(([^\)]+)\)"

    for m in re.compile(re_braced, re.MULTILINE).finditer(defsuffix):
        if '(' not in m.group(1):
            yield m


def text_parse_braced_or_identifier(text):
    brace_balance = 0
    text = text.strip()
    ret = ''

    if len(text):
        if text[0].isalnum() or text[0] in ['(',]:
            for t in text:
                should_break = brace_balance == 0 and t.isspace()

                if should_break:
                    break

                if '(' == t:
                    brace_balance -= 1
                elif ')' == t:
                    brace_balance += 1
                else:
                    ret += t

    return ret if 0 == brace_balance else ''


def text_remove_c_comments(text):
    return re.sub(r"/\\*.*?\\*/", "", text)


def text_parse_numeric_remove_suffix(text):
    return re.sub(r"\b((?:0x)?[0-9ABCDEF]+)UL?", r"\1", text)


def text_parse_define_kv(text):
    # re_valstring = r"^\#define" + RE_SPACE + RE_IDENTIFIER + RE_SPACE + '(' + RE_LINETERM + ')'
    re_valstring = r"^\#define" + RE_SPACE + RE_IDENTIFIER + RE_SPACE + r"([^\n]+)" + r"\n"

    for m in re.compile(re_valstring, re.MULTILINE).finditer(text):
        val = m.group(2)
        val = text_remove_c_comments(val)
        val = text_parse_braced_or_identifier(val)

        if len(val):
            yield m.group(1), text_parse_numeric_remove_suffix(val)


def text_parse_identifier(text):
    for m in re.compile(RE_IDENTIFIER, re.MULTILINE).finditer(text):
        yield m.group(1)


def kvlist_transform_remove_missing_identifiers(kvlist):
    keys = {kv[0] for kv in kvlist}

    for k, v in kvlist:
        identifiers = list(text_parse_identifier(v))

        if len(identifiers):
            if all([i in keys for i in identifiers]):
                yield k, v
        else:
            yield k, v


def kvlist_transform_uppercase(kvlist):
    for k, v in kvlist:
        key, value = k.upper(), v.upper()
        value = re.sub(r"\b0X", '0x', value)

        yield key, value


def kvlist_get_rustlines(kvlist):
    # pub const ADC_CFGR1_DISCEN_MSK: usize = 0x1usize << ADC_CFGR1_DISCEN_POS;
    for k, v in kvlist:
        yield f"pub const {k}: usize = {v};"



def main():
    text = command_output(f"cat {sys.argv[1]}")
    kvlist = list(text_parse_define_kv(text))
    kvlist = list(kvlist_transform_remove_missing_identifiers(kvlist))
    kvlist = list(kvlist_transform_uppercase(kvlist))
    kvlist = list(kvlist_get_rustlines(kvlist))

    for m in kvlist:
        print(m)


def main_legacy():
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
    content = replace_string_literals(content)  # Should be replaced w/ usize suffix for rust code generation
    content = replace_excessive_space(content)
    content = replace_define(content)
    content = parse_values(content)
    print(content)
    content = filter_missing_values(content)
    content = transform_identifiers_upper(content)
    content = replace_redundant_parenthesis(content)

    # print('\n'.join(generate_c_code(content)))
    return '\n'.join(generate_rust_code(content))

if __name__ == "__main__":
    main()
