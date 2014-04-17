import re
from PIL import Image, ImageDraw
from xml.etree.cElementTree import parse

try:
    import timing
except:
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
    found = re.findall("(\d+\.\d+) cm", text)
    if len(found):
        cm = float(found[0])
    else:
        # Try mm
        found = re.findall("(\d+\.\d+) mm", text)
        if len(found):
            cm = float(found[0]) / 10
        else:
            # Try m
            found = re.findall("(\d+\.\d+) m", text)
            if len(found):
                cm = float(found[0]) * 100
                # Avoid float('4.1') * 100 == 409.99999999999994
                cm = round(cm, 1)
    return cm


def get_sizes_from_xml():
    """Return list of all sizes and the max (w, h)"""
    filename = "fng-data-dc.xml"

    sizes = []

    print("Parse file")
    tree = parse(filename)
    root = tree.getroot()

    print("Find")

    max_w = 0
    max_h = 0

    for child in root:
        artwork = False
        height = None
        width = None

        for grandchild in child:
            if grandchild.tag == "{http://purl.org/dc/elements/1.1/}type":
                # print grandchild.tag
                # print grandchild.attrib
                # print grandchild.text
                if grandchild.text == "artwork":
                    artwork = True
                elif grandchild.text == "artist":
                    break

            elif grandchild.tag == "{http://purl.org/dc/elements/1.1/}format":
                # print grandchild.tag
                # print grandchild.attrib
                # print grandchild.text
                if grandchild.attrib == {'type': 'dimension'}:
                    if grandchild.text.startswith("leveys"):
                        width = grandchild.text
                    elif grandchild.text.startswith("korkeus"):
                        height = grandchild.text

        if artwork:
            if width and height:
                w = get_cm(width)
                h = get_cm(height)
                if w and h:
                    sizes.append((w, h))
                    if w > max_w:
                        max_w = w
                    if h > max_h:
                        max_h = h

    return sizes, max_w, max_h


def plot_sizes(sizes, max_w, max_h):
    """sizes is a list of (width, height)"""
    im = Image.new('RGB', (int(max_w * 1.1), int(max_h * 1.1)), "white")
    draw = ImageDraw.Draw(im)

    for s in sizes:
        # Centre it
        x0 = (im.size[0] - s[0]) / 2
        x1 = x0 + s[0]
        y0 = (im.size[1] - s[1]) / 2
        y1 = y0 + s[1]
        draw.rectangle([(x0, y0), (x1, y1)], outline="black")

    im.save("out.png")


if __name__ == '__main__':

    sizes, max_w, max_h = get_sizes_from_xml()

    print len(sizes)
    print max_w, max_h

    plot_sizes(sizes, max_w, max_h)

# End of file
