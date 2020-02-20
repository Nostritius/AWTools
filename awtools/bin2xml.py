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
import math

from struct import unpack, pack
import xml.etree.ElementTree as ET
from xml.dom import minidom

class DataType(enum.Enum):
    EMPTY = 0x00000000
    RID = 0x00000018
    FILE_INFO = 0x00000020
    CELL_INFO = 0x00000024
    TEXTURE_METADATA = 0x0000006D
    STATIC_OBJECT = 0x00000089


STRUCT_ID = 0xEFBEADDE
CELL_SLOT_ID = 0xE9A6EC14

RID_ID = 0x8F2362B8
UNKNOWN_1_ID = 0x9B622683
TASK_DEFINITION_ID = 0xD5488A35
POSITION_ID = 0x9B622683

f = open(sys.argv[1], "rb")

f.seek(0, 2)
file_size = f.tell()
f.seek(0)

magic_id = unpack('I', f.read(4))[0] # ?
unknown1 = unpack('I', f.read(4))[0]
num_elements = unpack('I', f.read(4))[0]
unknown2 = unpack('I', f.read(4))[0]

root_node = ET.Element("data")

root_node.set("id", hex(magic_id))


def write_cell_slot(f, node):
    cell_slot_node = ET.SubElement(node, "cell_slot")

    unknown = unpack('I', f.read(4))[0]
    cell_x = unpack('I', f.read(4))[0]
    cell_y = unpack('I', f.read(4))[0]

    cell_slot_node.set("cell_x", str(cell_x))
    cell_slot_node.set("cell_y", str(cell_y))

    zero1 = unpack('I', f.read(4))[0]
    zero2 = unpack('I', f.read(4))[0]


def write_transform(f, node):
    transform_node = ET.SubElement(node, "transform")

    unknown1 = unpack('I', f.read(4))[0] # Always 10?
    sx = unpack('f', f.read(4))[0]  # Probably a hash?
    sy = unpack('f', f.read(4))[0]  # Always 0?
    sz = unpack('f', f.read(4))[0]  # Probably a hash?

    qx = unpack('f', f.read(4))[0]
    qy = unpack('f', f.read(4))[0]
    qz = unpack('f', f.read(4))[0]
    angle = unpack('f', f.read(4))[0]

    unknown2 = unpack('f', f.read(4))[0]
    unknown3 = unpack('f', f.read(4))[0]

    x = unpack('f', f.read(4))[0]
    y = unpack('f', f.read(4))[0]
    z = unpack('f', f.read(4))[0]

    position_node = ET.SubElement(transform_node, "position")

    position_node.set("x", str(x))
    position_node.set("y", str(y))
    position_node.set("z", str(z))

    rotation_node = ET.SubElement(transform_node, "rotation")

    rotation_node.set("x", str(qx))
    rotation_node.set("y", str(qy))
    rotation_node.set("z", str(qz))
    rotation_node.set("angle", str(angle))

    rotation_node2 = ET.SubElement(transform_node, "rotation")

    rotation_node2.set("yaw", str(math.degrees(sx)))
    rotation_node2.set("pitch", str(sy))
    rotation_node2.set("roll", str(math.degrees(sz)))
    rotation_node2.set("unknown1", str(math.degrees(unknown2)))
    rotation_node2.set("unknown2", str(math.degrees(unknown3)))


def write_rid(f, node):
    rid_node = ET.SubElement(node, "rid")

    type = unpack('>I', f.read(4))[0]
    if type != RID_ID:
        raise Exception("Invalid rid info")

    num_rids = unpack('I', f.read(4))[0]  # ?
    rid = unpack('>I', f.read(4))[0]

    rid_node.set("id", hex(rid))


def write_cell_info(f, node):
    type = unpack('>I', f.read(4))[0]
    if type != CELL_SLOT_ID:
        raise Exception("Invalid cell info")

    write_cell_slot(f, node)


def write_static_object(f, node):
    type = unpack('>I', f.read(4))[0]
    if type != POSITION_ID:
        raise Exception("Invalid static object")

    write_transform(f, node)

    write_struct(f, node, True)
    write_struct(f, node, True)
    write_struct(f, node, True)
    write_struct(f, node, True)

    f.seek(13, 1)


def write_struct(f, node, substruct=False):
    begin_marker = unpack('>I', f.read(4))[0]

    t = DataType(unpack('I', f.read(4))[0])

    strct_node = ET.SubElement(node, "struct")
    strct_node.set("type", t.name)

    if t == DataType.CELL_INFO:
        write_cell_info(f, strct_node)
    elif t == DataType.STATIC_OBJECT:
        write_static_object(f, strct_node)
    elif t == DataType.RID:
        write_rid(f, strct_node)

    if not substruct:
        end_marker = unpack('I', f.read(4))[0]


for i in range(num_elements):
    write_struct(f, root_node)

print(minidom.parseString(ET.tostring(root_node)).toprettyxml(indent="\t"))
