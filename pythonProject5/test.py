from urllib.parse import unquote
from urllib.parse import quote
name = 'M4A1 消音型 | 暴怒野兽 (久经沙场)'
strName = '+'
name = quote(name).replace('%20','+')
name = name.replace('%28','(')
name = name.replace('%29',')')
print(name == 'M4A1+%E6%B6%88%E9%9F%B3%E5%9E%8B+%7C+%E6%9A%B4%E6%80%92%E9%87%8E%E5%85%BD+(%E4%B9%85%E7%BB%8F%E6%B2%99%E5%9C%BA)')
# print(strName.join())
print(unquote('M4A1+%E6%B6%88%E9%9F%B3%E5%9E%8B+%7C+%E6%9A%B4%E6%80%92%E9%87%8E%E5%85%BD+(%E4%B9%85%E7%BB%8F%E6%B2%99%E5%9C%BA)'))