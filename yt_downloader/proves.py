import re

m = re.search("Your number is <b>(\d+)</b>",
      "xxx Your number is <b>sfqdas1245asdf2</b>  fdjsk")
if m:
    print(m.groups()[0])