#!/usr/bin/env python3
"""
Show top 25 artists represented in the FNG collection.

From 19 Nov 2019:

Found 39995 artworks with artists

1. Palsa, Kalervo (3038)
2. tuntematon (1432)
3. Pietilä, Tuulikki (1431)
4. Edelfelt, Albert (1319)
5. Soldan-Brofeldt, Venny (1267)
6. Sjöstrand, Carl Eneas (995)
7. Simberg, Hugo (807)
8. Gallen-Kallela, Akseli (464)
9. Kuusi, Helmi (430)
10. Kaskipuro, Pentti (395)
11. Thomé, Verner (382)
12. Ekman, Robert Wilhelm (381)
13. Finch, Alfred William (365)
14. Kunisada (364)
15. Holmberg, Werner (354)
16. Kleineh, Oscar (350)
17. Visanti, Matti (341)
18. Wright, Magnus von (319)
19. Enckell, Magnus (288)
20. Järnefelt, Eero (280)
21. Helenius, Ester (276)
22. Sparre, Louis (262)
23. Mikkonen, Aune (261)
24. Godenhjelm, Berndt Abraham (213)
25. Wiik, Maria (206)

"""
from collections import Counter
from xml.etree.cElementTree import parse

try:
    import timing

    assert timing  # silence warnings
except ImportError:
    pass


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
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
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


if __name__ == "__main__":

    artists = get_artists_from_xml()
    print("Found", len(artists), "artworks with artists")
    top = most_frequent_with_counts(artists, 25)
    for i, (artist, count) in enumerate(top):
        print(str(i + 1) + ". " + artist + " (" + str(count) + ")")

# End of file
