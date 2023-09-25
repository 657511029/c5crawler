import re
import json
import requests
from lxml import etree
from urllib.parse import quote
from urllib.parse import unquote
import time
import xlsxwriter as xw
import os
name = 'USP 消音版 | 地狱门票 (崭新出厂)'
name = quote(name)
name = name.replace('%7C','|')
name = name.replace('%28','(')
name = name.replace('%29',')')
print(name)
print('USP%20%E6%B6%88%E9%9F%B3%E7%89%88%20|%20%E5%9C%B0%E7%8B%B1%E9%97%A8%E7%A5%A8%20(%E5%B4%AD%E6%96%B0%E5%87%BA%E5%8E%82)' == name)