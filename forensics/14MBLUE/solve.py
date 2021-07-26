import re
from base64 import b64decode
import zlib
from pwn import xor

pattern1 = "0558c2fe7378"
pattern2 = "a403360fc656"
key = b"f74cd7bf"


coms = open("coms", "r").readlines()


def decode_base64(data, altchars=b"+/"):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb"[^a-zA-Z0-9%s]+" % altchars, b"", data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b"=" * (4 - missing_padding)
    return b64decode(data, altchars)


for line in coms:
    group = re.findall(pattern1 + r"(.*)" + pattern2, line.strip())
    if len(group) > 0:
        found = group[0]
        print(zlib.decompress(xor(decode_base64(found.encode()), key)))
