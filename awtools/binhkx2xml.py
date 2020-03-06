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

import xml.etree.ElementTree as ET

from struct import unpack
from xml.dom import minidom

f = open(sys.argv[1], "rb")

root_node = ET.Element("havok")

magic_id_1 = unpack('I', f.read(4))[0]
magic_id_2 = unpack('I', f.read(4))[0]

if magic_id_1 != 0x57e0e057 or magic_id_2 != 0x10c0c010:
    raise Exception("Invalid magic id")

user_tag = unpack('I', f.read(4))[0]
file_version = unpack('I', f.read(4))[0]

f.seek(4, 1)  # Structure layout rules

num_sections = unpack('I', f.read(4))[0]

contents_section_index = unpack('I', f.read(4))[0]
contents_section_offset = unpack('I', f.read(4))[0]

class_name_section_index = unpack('I', f.read(4))[0]
class_name_section_offset = unpack('I', f.read(4))[0]

f.seek(16, 1)  # Reserved

flags = unpack('I', f.read(4))[0]

f.seek(4, 1)  # Pad

class_names = {}

for i in range(num_sections):
    section_name = unpack('<19s', f.read(19))[0].decode("ascii").replace("\0", "")
    f.seek(1, 1)

    absolute_data_start = unpack('I', f.read(4))[0]
    local_fixups_offset = unpack('I', f.read(4))[0]
    global_fixups_offset = unpack('I', f.read(4))[0]
    virtual_fixups_offset = unpack('I', f.read(4))[0]
    exports_offset = unpack('I', f.read(4))[0]
    imports_offset = unpack('I', f.read(4))[0]
    end_offset = unpack('I', f.read(4))[0]

    section_node = ET.SubElement(root_node, "section", {"type": section_name})

    last_pos = f.tell()

    f.seek(absolute_data_start)

    if section_name == "__classnames__":
        while True:
            tag = unpack('I', f.read(4))
            if tag == 0xFFFFFFFF:
                break


    elif section_name == "__types__":
        pass
    elif section_name == "__data__":
        pass


    f.seek(last_pos)



print(minidom.parseString(ET.tostring(root_node)).toprettyxml(indent="\t"))
