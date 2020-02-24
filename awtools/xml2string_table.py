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

from struct import pack
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()

strings = []

for child in root:
    if child.tag != "string":
        raise Exception("Invalid xml tag")

    strings.append(child.attrib)

f = open(sys.argv[2], "wb")

f.write(pack('I', len(strings)))

for string in strings:
    id = string["id"]
    value = string["value"]

    f.write(pack('I', len(id)))
    f.write(bytearray(id, "ascii"))

    f.write(pack('I', len(value)))
    f.write(bytearray(value, "utf-16le"))

f.close()
