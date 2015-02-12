#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Show top 25 artists represented in the FNG collection.

From 12 Feb 2015:

Found 36945 artworks with artists

1. Palsa, Kalervo (3036)
2. tuntematon (1393)
3. Edelfelt, Albert (1318)
4. Soldan-Brofeldt, Venny (1267)
5. Sjöstrand, Carl Eneas (994)
6. Simberg, Hugo (804)
7. Gallen-Kallela, Akseli (464)
8. Kuusi, Helmi (430)
9. Thomé, Verner (381)
10. Ekman, Robert Wilhelm (380)
11. Kunisada (365)
12. Finch, Alfred William (364)
13. Holmberg, Werner (354)
14. Kleineh, Oscar (349)
15. Visanti, Matti (341)
16. Wright, Magnus von (315)
17. Enckell, Magnus (288)
18. Helenius, Ester (276)
19. Järnefelt, Eero (270)
20. Mikkonen, Aune (261)
21. Sparre, Louis (261)
22. Godenhjelm, Berndt Abraham (213)
23. Wiik, Maria (206)
24. Jansson, Karl Emanuel (203)
25. Schjerfbeck, Helene (201)

"""
from __future__ import print_function
from __future__ import unicode_literals
from collections import Counter
from xml.etree.cElementTree import parse

try:
    import timing
    assert timing  # silence warnings
except:
    pass


# Windows cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode('utf-8'))


def get_artists_from_xml():
    """Return list of all artists"""
    filename = "fng-data-dc.xml"

    creators = []  # aka artists

    print("Parse file")
    tree = parse(filename)
    root = tree.getroot()

    print("Find")

    for child in root:
        artwork = False
        creator = None

        for grandchild in child:
            if grandchild.tag == "{http://purl.org/dc/elements/1.1/}type":
                # print grandchild.tag
                # print grandchild.attrib
                # print grandchild.text
                if grandchild.text == "artwork":
                    artwork = True
                elif grandchild.text == "artist":
                    break

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}creator":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                # if grandchild.attrib == {'type': 'c'}:
                creator = grandchild.text

        if artwork:
            if creator:
                creators.append(creator)

    return creators


def most_frequent_with_counts(some_list, number=None):
    print("Find most common")
    counter = Counter(some_list)
    most_common = counter.most_common(number)
    return most_common


if __name__ == '__main__':

    artists = get_artists_from_xml()
    print("Found", len(artists), "artworks with artists")
    top = most_frequent_with_counts(artists, 25)
    for i, (artist, count) in enumerate(top):
        print_it(str(i+1) + ". " + artist + " (" + str(count) + ")")

# End of file
