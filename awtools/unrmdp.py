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
import os

from struct import unpack

fbin = open(sys.argv[1], "rb")
frmdp = open(sys.argv[2], "rb")

magic_id = unpack('B', fbin.read(1))[0]

root_path_length = 7

# Alan Wake
if magic_id == 1:
    fbin.seek(4, 1)

    num_folders = unpack('>I', fbin.read(4))[0]
    num_files = unpack('>I', fbin.read(4))[0]

    name_size = unpack('>I', fbin.read(4))[0]

    endianness = ">"

# Alan Wakes American Nightmare
elif magic_id == 0:
    root_path_length = unpack('I', fbin.read(4))[0]

    num_folders = unpack('I', fbin.read(4))[0]
    num_files = unpack('I', fbin.read(4))[0]

    fbin.seek(8, 1)

    name_size = unpack('I', fbin.read(4))[0]

    endianness = "<"

fbin.seek(root_path_length + 1, 1)
fbin.seek(120, 1)

folderNames = []
folders = []
prevIds = []


def get_name(f, name_offset):
    last_pos = f.tell()

    f.seek(-name_size + name_offset, 2)

    name = ""
    c = unpack('c', f.read(1))[0].decode('ascii')
    while c != '\0':
        name += c
        c = unpack('c', f.read(1))[0].decode('ascii')

    f.seek(last_pos)

    return name


for i in range(num_folders):
    fbin.seek(8, 1)
    prev_id = unpack(endianness + 'I', fbin.read(4))[0]
    fbin.seek(4, 1)
    name_offset = unpack(endianness + 'I', fbin.read(4))[0]
    fbin.seek(8, 1)

    if name_offset != 0xFFFFFFFF:
        folderNames.append(get_name(fbin, name_offset))
    else:
        folderNames.append("")
    prevIds.append(prev_id)

for i in range(num_folders):
    name = folderNames[i]
    prev_id = prevIds[i]
    while prev_id != 0xFFFFFFFF:
        if folderNames[prev_id] != "":
            name = folderNames[prev_id] + "/" + name
        prev_id = prevIds[prev_id]

    folders.append(name)

    if name != "":
        os.makedirs(name, exist_ok=True)

pos = fbin.tell()

for i in range(num_files):
    fbin.seek(8, 1)
    prev_id = unpack(endianness + 'I', fbin.read(4))[0]
    flags = unpack(endianness + 'I', fbin.read(4))[0]
    name_offset = unpack(endianness + 'I', fbin.read(4))[0]
    offset = unpack(endianness + 'Q', fbin.read(8))[0]
    size = unpack(endianness + 'Q', fbin.read(8))[0]
    crc = unpack(endianness + 'I', fbin.read(4))[0]

    if magic_id == 0:
        fbin.seek(8, 1)

    name = get_name(fbin, name_offset)

    nf = open(folders[prev_id] + "/" + name, "wb")

    frmdp.seek(offset)
    data = frmdp.read(size)

    nf.write(data)
    nf.close()

