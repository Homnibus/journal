def java_string_hashcode(string):
    hash = 0
    for c in string:
        hash = (31 * hash + ord(c)) & 0xFFFFFFFF
    return ((hash + 0x80000000) & 0xFFFFFFFF) - 0x80000000    