import re

entries = ['CSS', 'Django', 'Git', 'HTML', 'Python']

m = 'css'

print(re.findall(r"^?c", 'CSS', flags=re.IGNORECASE))
