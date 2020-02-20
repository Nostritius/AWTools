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
import enum

from struct import unpack
import xml.etree.ElementTree as ET
from xml.dom import minidom

f = open(sys.argv[1], "rb")

num_elements = unpack('I', f.read(4))[0]
f.seek(8, 1)
name_size = unpack('I', f.read(4))[0]

root_node = ET.Element("packmeta")

names = []
for i in range(num_elements):
    name = ""
    c = unpack('c', f.read(1))[0].decode('ascii')
    while c != '\0':
        name += c
        c = unpack('c', f.read(1))[0].decode('ascii')

    print(name)
    names.append(name)

name_offsets = []
for i in range(num_elements):
    name_offset = unpack('I', f.read(4))[0]
    name_offsets.append(name_offset)

rid_count = unpack('I', f.read(4))[0]
rids = []
rid_to_name = []
for i in range(rid_count):
    rids.append(unpack('>I', f.read(4))[0])

for i in range(rid_count):
    rid_to_name.append(unpack('I', f.read(4))[0])

for i in range(num_elements):
    r = ET.SubElement(root_node, "resource")
    r.set("name", names[i])

    name_offset = name_offsets[i]
    if name_offset in rid_to_name:
        r.set("rid", hex(rids[rid_to_name.index(name_offset)]))

print(minidom.parseString(ET.tostring(root_node)).toprettyxml(indent="\t"))
