#!/bin/python3

# This file is part of AWTools.
#
# AWTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AWTools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AWTools.  If not, see <https://www.gnu.org/licenses/>.

import sys

from struct import unpack
import xml.etree.ElementTree as ET
from xml.dom import minidom

f = open(sys.argv[1], "rb")

root_node = ET.Element("binfnt")

magic_id = unpack('I', f.read(4))[0]

num_glyphs = unpack('I', f.read(4))[0]
glyph_node = ET.SubElement(root_node, "glyph_coordinates")

for i in range(num_glyphs):
    vertex_x = str(unpack('f', f.read(4))[0])
    vertex_y = str(unpack('f', f.read(4))[0])
    s = str(unpack('f', f.read(4))[0])
    t = str(unpack('f', f.read(4))[0])

    ET.SubElement(
        glyph_node,
        "glyph_coordinate",
        {"x": vertex_x, "y": vertex_y, "s": s, "t": t}
    )

num_indexes = unpack('I', f.read(4))[0]
indices_node = ET.SubElement(root_node, "indices")
for i in range(num_indexes):
    index = str(unpack('H', f.read(2))[0])
    ET.SubElement(indices_node, "index", {"index": index})

num_glyphs2 = unpack('I', f.read(4))[0]
glyph_node = ET.SubElement(root_node, "glyphs")
for i in range(num_glyphs2):
    vertex_offset = str(unpack('H', f.read(2))[0])
    vertex_count = str(unpack('H', f.read(2))[0])
    index_offset = str(unpack('H', f.read(2))[0])
    index_count = str(unpack('H', f.read(2))[0])

    ET.SubElement(glyph_node, "glyph", {
        "vertex_offset": vertex_offset,
        "vertex_count": vertex_count,
        "index_offset": index_offset,
        "index_count": index_count,
    })

    f.seek(36, 1)

# Character list
f.seek(0x20000, 1)

print(minidom.parseString(ET.tostring(root_node)).toprettyxml(indent="\t"))

texture_size = unpack('I', f.read(4))[0]

ftex = open(sys.argv[1] + ".dds", "wb")
ftex.write(f.read(texture_size))
ftex.close()
