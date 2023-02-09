import re

# 从一段文本中摘取数字
def getnumber(aa):
    numbers = re.findall("\d+", aa)
    number = "".join(numbers)
    return number


word = "自然资函〔2019〕419号"
print(getnumber(word))
