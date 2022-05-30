import re
regex = "^[a-zA-Z0-9]{1,16}$"
pattern = re.compile(regex)
text = 'фыав'
if pattern.search(text) is True:
    print("OK")
