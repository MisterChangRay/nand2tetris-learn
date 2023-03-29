import sys
import re
import os
from pathlib import Path

tokenTmp3 = r"({|}|\(|\)|\[|\]|\.|,|;|\+|-|\*|/|&|\||<|>|=|~|class|constructor|function|method|field|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)"
tokenTmp3 ="(.*?)?" + tokenTmp3 + "(.*?)?" + tokenTmp3 + "?"


tokenTmp4 = r"(var|return)"

print(re.findall(tokenTmp3, "a=a+b;"))

print(re.findall(tokenTmp3, "class z{;"))
print(re.findall(tokenTmp3, " {"))