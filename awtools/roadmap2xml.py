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

root_node = ET.Element("roadmap")

version = unpack('I', f.read(4))[0]
f.seek(4,1)

num_roads = unpack('I', f.read(4))[0]

for i in range(num_roads):
    road_node = ET.SubElement(root_node, "road")

    num_blocks = unpack('I', f.read(4))[0]
    length = unpack('f', f.read(4))[0]
    width = unpack('f', f.read(4))[0]

    road_node.attrib = {
        "length":str(length),
        "width":str(width)
    }

    for i in range(num_blocks):
        block_node = ET.SubElement(road_node, "block")

        x = unpack('f', f.read(4))[0]
        y = unpack('f', f.read(4))[0]
        z = unpack('f', f.read(4))[0]

        block_node.attrib = {
            "x": str(x),
            "y": str(y),
            "z": str(z)
        }

end_tag = unpack('I', f.read(4))[0]  # 0x67f90200

print(minidom.parseString(ET.tostring(root_node)).toprettyxml(indent="\t"))