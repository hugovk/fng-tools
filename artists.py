#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import re
from xml.etree.cElementTree import parse

try:
    import timing

    assert timing  # silence warnings
except ImportError:
    pass


# Windows cmd.exe cannot do Unicode so encode first
def print_it(text):
    print(text.encode("utf-8"))


def year_from_date(date):
    year = None
    if date is None:
        return None

    match = re.search(r"\d\d\d\d", date)
    if match:
        year = int(match.group(0))

    return year


def artist_data_from_xml():
    """
    Return list of artists. Each artist is:
    [name, birthplace, birthdate, death place, death date]
    """
    filename = "fng-data-dc.xml"

    artists = []

    print("Parse file")
    tree = parse(filename)
    root = tree.getroot()

    print("Find")

    min_birth_year = 9999
    max_birth_year = 0
    min_death_year = 9999
    max_death_year = 0

    for child in root:
        artist = False
        name = None
        birthdate = None
        birthplace = None
        deathdate = None
        deathplace = None

        # http://kokoelmat.fng.fi/api/v2support/docs/#/documentation

        for grandchild in child:
            if grandchild.tag == "{http://purl.org/dc/elements/1.1/}type":
                if grandchild.text == "artist":
                    artist = True
                elif grandchild.text == "artwork":
                    break

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}title":
                # print(1, grandchild.tag)
                # print(2, grandchild.attrib)
                # print_it("3 " + grandchild.text)
                name = grandchild.text

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}date":
                if grandchild.attrib["type"] == "birth":
                    birthdate = grandchild.text
                    if "loc" in grandchild.attrib:
                        birthplace = grandchild.attrib["loc"]
                if grandchild.attrib["type"] == "death":
                    deathdate = grandchild.text
                    if "loc" in grandchild.attrib:
                        deathplace = grandchild.attrib["loc"]

        # {http://purl.org/dc/elements/1.1/}date
        # {'loc': 'Tampere', 'type': 'birth'}
        # 1907-03-08

        # {http://purl.org/dc/elements/1.1/}date
        # {'loc': 'Tampere', 'type': 'death'}
        # 1999-11-18

        if artist:

            birth_year = year_from_date(birthdate)
            death_year = year_from_date(deathdate)

            # Skip bad data
            if (
                (name == "Tampere")
                or (name == "Milano")
                or (name == "Moskova, Venäjä")
                or (birth_year and death_year and death_year < birth_year)
                or (birthdate == deathdate)
                or (birth_year == death_year)
                or (birth_year == 180 and death_year == 1682)
                or (birthdate == "(1100 - 1874)" and deathdate == "(1100 - 1989)")
                or (birthdate == "(1000 - 1916)")
            ):
                continue
            if death_year and birth_year:
                if death_year - birth_year > 150:
                    continue

            if birth_year:
                if birth_year < min_birth_year:
                    min_birth_year = birth_year
                if birth_year > max_birth_year:
                    max_birth_year = birth_year
            if death_year:
                if death_year < min_death_year:
                    min_death_year = death_year
                if death_year > max_death_year:
                    max_death_year = death_year

            artists.append([name, birthdate, birthplace, deathdate, deathplace])

    print(min_birth_year)
    print(max_birth_year)
    print(min_death_year)
    print(max_death_year)

    return artists


if __name__ == "__main__":

    artists = artist_data_from_xml()

    print("Total:\t", len(artists))

# End of file
