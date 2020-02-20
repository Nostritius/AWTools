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

root_node = ET.Element("string_table")

num_strings = unpack('I', f.read(4))[0]


def read_string_ascii():
    length = unpack('I', f.read(4))[0]
    return unpack("<" + str(length) + "s", f.read(length))[0].decode('ascii')


def read_string_utf16():
    length = unpack('I', f.read(4))[0]
    return unpack("<" + str(length * 2) + "s", f.read(length * 2))[0].decode('utf-16le')


for i in range(num_strings):
    sid = read_string_ascii()
    value = read_string_utf16()

    string_node = ET.SubElement(root_node, "string", {"id": sid, "value": value})

print(minidom.parseString(ET.tostring(root_node)).toprettyxml(indent="\t"))
