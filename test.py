# -*- coding: UTF-8 -*-

import re

regexes = [
    "([A-Za-z\-'\. ]*) as ([A-Za-z\-'\. ]*)",
    "([\p{L}\-'\. ]*) as ([\p{L}\-'\. ]*)",
    "([A-Za-z\-'\.^\W\d_ ]*) as ([A-Za-z\-'\.^\W\d_ ]*)",
    "([\w\-'\. ]*) as ([\w\-'\. ]*)",
    "([^0-9\(]*) as ([^0-9\(]*)"
]

strings = [
    "Peter Dinklage as Tyrion Lannister",
    "Daniel Naprous as Oznak zo Pahl(credited as Stunt Performer)",
    "Filip Lozić as Young Nobleman",
    "Morgan C. Jones as a Braavosi captain",
    "Adewale Akinnuoye-Agbaje as Malko"
]

for regex in regexes:
    print regex
    for string in strings:
        print string
        match = re.match( regex, string)
        if match is not None:
            print match.groups()
        else:
            print "FAIL"
        print ""
    print ""
