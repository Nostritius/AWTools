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

root_node = ET.Element("dp")

numValues = unpack("I",  f.read(4))[0]
numReferences = unpack("I",  f.read(4))[0]
numStrings = unpack("I", f.read(4))[0]
dataSize = unpack("I", f.read(4))[0]

f.seek(12, 1)

data_offset = 28 + numValues * 4 + numStrings * 4

bytecodeOffsets = []
for i in range(numReferences):
    bytecodeOffsets.append(unpack("I", f.read(4))[0])

valueOffsets = []
for i in range(numValues):
    valueOffsets.append(unpack("I", f.read(4))[0])

valueStrings = []
for i in range(numStrings):
    valueStrings.append(unpack("I", f.read(4))[0])


bytecode_node = ET.SubElement(root_node, "bytecode")

for bytecode_offset in bytecodeOffsets:
    pass

value_node = ET.SubElement(root_node, "values")

for valueOffset in valueOffsets:
    pass

strings_node = ET.SubElement(root_node, "strings")

for valueString in valueStrings:
    overlap = (valueString & 0x80) != 0

    offset = valueString >> 8

    offset *= 8
    if overlap:
        offset += 4

    f.seek(-dataSize + offset, 2)

    string = ""
    c = unpack('c', f.read(1))[0].decode('ascii')
    while c != '\0':
        string += c
        c = unpack('c', f.read(1))[0].decode('ascii')

    ET.SubElement(strings_node, "string", {"id": hex(valueString), "value": str(string)})

print(minidom.parseString(ET.tostring(root_node, encoding="ascii", method="xml")).toprettyxml(indent="\t"))
