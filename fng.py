#!/usr/bin/env python3
"""
Plot the sizes of all the artworks in the Finnish National Gallery.

Example output:
https://www.flickr.com/photos/hugovk/albums/72157644045546102
https://www.flickr.com/photos/tags/fngpy
"""
import argparse
import re
from PIL import Image, ImageDraw
from xml.etree.cElementTree import parse

try:
    import timing

    assert timing  # silence warnings
except ImportError:
    pass


def get_cm(text):
    # Examples:
    # 'leveys 59,00 cm', 'korkeus 41,50 cm'
    # u'leveys p\xe4iv\xe4mitta 30,00 cm',
    # u'korkeus, p\xe4iv\xe4mitta 23,80 cm'
    # 'leveys 10,50 cm', 'korkeus 7,50 cm'
    # None, 'korkeus 72,50 cm'

    cm = None
    if text is None:
        return None

    text = text.replace(",", ".")

    # Try cm
    found = re.findall(r"(\d+\.\d+) cm", text)
    if len(found):
        cm = float(found[0])
    else:
        # Try mm
        found = re.findall(r"(\d+\.\d+) mm", text)
        if len(found):
            cm = float(found[0]) / 10
        else:
            # Try m
            found = re.findall(r"(\d+\.\d+) m", text)
            if len(found):
                cm = float(found[0]) * 100
                # Avoid float('4.1') * 100 == 409.99999999999994
                cm = round(cm, 1)
    return cm


def get_sizes_from_xml(filename, limit=None):
    """Return list of all sizes and the max (w, h)"""
    sizes = []

    print("Parse file")
    tree = parse(filename)
    root = tree.getroot()

    print("Find")

    max_w = 0
    max_h = 0

    if limit:
        limit = float(limit)

    for child in root:
        artwork = False
        height = None
        width = None

        for grandchild in child:
            if grandchild.tag == "{http://purl.org/dc/elements/1.1/}type":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                if grandchild.text == "artwork":
                    artwork = True
                elif grandchild.text == "artist":
                    break

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}format":
                # print(grandchild.tag)
                # print(grandchild.attrib)
                # print(grandchild.text)
                if grandchild.attrib == {"type": "dimension"}:
                    if grandchild.text.startswith("leveys"):
                        width = grandchild.text
                    elif grandchild.text.startswith("korkeus"):
                        height = grandchild.text

        if artwork:
            if width and height:
                w = get_cm(width)
                h = get_cm(height)
                if w and h:
                    if not limit or (w < limit and h < limit):
                        sizes.append((w, h))
                        if w > max_w:
                            max_w = w
                        if h > max_h:
                            max_h = h

    return sizes, max_w, max_h


def stats(sizes):
    print("Get stats")
    widths = [s[0] for s in sizes]
    heights = [s[1] for s in sizes]

    w_avg = sum(widths) / float(len(widths))
    h_avg = sum(heights) / float(len(heights))
    print("Avg:\t", w_avg, "x", h_avg, "cm")

    try:
        from collections import Counter

        data = Counter(widths)
        w_mode = data.most_common(1)[0][0]
        data = Counter(heights)
        h_mode = data.most_common(1)[0][0]
        print("Mode:\t", w_mode, "x", h_mode, "cm")
    except ImportError:
        pass


def centred(w, h, big_size):
    big_w, big_h = big_size

    x0 = (big_w - w) / 2
    x1 = x0 + w
    y0 = (big_h - h) / 2
    y1 = y0 + h

    return [(x0, y0), (x1, y1)]


def plot_sizes(sizes, max_w, max_h, scale):
    """sizes is a list of (width, height)"""
    print("Plot sizes")
    im = Image.new("RGB", (int(max_w / scale * 1.1), int(max_h / scale * 1.1)), "white")
    draw = ImageDraw.Draw(im)

    for (w, h) in sizes:
        draw.rectangle(centred(w / scale, h / scale, im.size), outline="black")

    im.save("out.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot the sizes of all artworks in the Finnish National Gallery",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-x", "--xml", default="fng-data-dc.xml", help="Input XML file")
    parser.add_argument(
        "-l",
        "--limit",
        default=None,
        metavar="cm",
        help="Limit to artworks smaller than this",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=float,
        default=1,
        metavar="cm per pixel",
        help="Scale of output image. Use 0.2 cm/px for larger, more detailed output.",
    )
    args = parser.parse_args()

    sizes, max_w, max_h = get_sizes_from_xml(args.xml, args.limit)

    print("Total:\t", len(sizes))
    print("Max:\t", max_w, "x", max_h, "cm")

    stats(sizes)

    plot_sizes(sizes, max_w, max_h, args.scale)

# End of file
