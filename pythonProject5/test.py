from urllib.parse import unquote
from urllib.parse import quote
name = 'M4A1 消音型 | 暴怒野兽 (久经沙场)'
strName = '+'
name = quote(name).replace('%20','+')
name = name.replace('%28','(')
name = name.replace('%29',')')
print(int('1000'))