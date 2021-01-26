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
import zlib
import datetime

from struct import unpack

fbin = open(sys.argv[1], "rb")
frmdp = open(sys.argv[2], "rb")

endianness_id = unpack('B', fbin.read(1))[0]
if endianness_id == 1:
    endianness = ">"
else:
    endianness = "<"

version = unpack(endianness + 'I', fbin.read(4))[0]

root_path_length = 7

num_folders = unpack(endianness + 'I', fbin.read(4))[0]
num_files = unpack(endianness + 'I', fbin.read(4))[0]

# Alan Wake
if version == 2:
    name_size = unpack('>I', fbin.read(4))[0]

    fbin.seek(8, 1)
    fbin.seek(120, 1)

# Alan Wakes American Nightmare
elif version == 7:
    fbin.seek(8, 1)

    name_size = unpack('I', fbin.read(4))[0]

    fbin.seek(8, 1)
    fbin.seek(120, 1)

# Quantum Break
elif version == 8:
    fbin.seek(8, 1)

    name_size = unpack('I', fbin.read(4))[0]

    fbin.seek(8, 1)
    fbin.seek(120, 1)

# Control
elif version == 9:
    fbin.seek(8, 1)

    name_size = unpack('I', fbin.read(4))[0]

    fbin.seek(128, 1)

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
    crc = unpack(endianness + 'I', fbin.read(4))[0]
    if version >= 8:
        next_neighbour_folder_id = unpack(endianness + 'Q', fbin.read(8))[0]
        prev_id = unpack(endianness + 'Q', fbin.read(8))[0]
    else:
        next_neighbour_folder_id = unpack(endianness + 'I', fbin.read(4))[0]
        prev_id = unpack(endianness + 'I', fbin.read(4))[0]

    fbin.seek(4, 1)

    if version >= 8:
        name_offset = unpack(endianness + 'Q', fbin.read(8))[0]
        next_lower_folder_id = unpack(endianness + 'Q', fbin.read(8))[0]
        next_file_id = unpack(endianness + 'Q', fbin.read(8))[0]
    else:
        name_offset = unpack(endianness + 'I', fbin.read(4))[0]
        next_lower_folder_id = unpack(endianness + 'I', fbin.read(4))[0]
        next_file_id = unpack(endianness + 'I', fbin.read(4))[0]

    if name_offset != 0xFFFFFFFF and name_offset != 0xFFFFFFFFFFFFFFFF:
        folderName = get_name(fbin, name_offset)
    else:
        folderName = ""

    if zlib.crc32(bytearray(folderName.lower(), "ascii")) != crc:
        raise Exception("Invalid folder name crc checksum")

    folderNames.append(folderName)
    prevIds.append(prev_id)

for i in range(num_folders):
    name = folderNames[i]
    prev_id = prevIds[i]
    while prev_id != 0xFFFFFFFF and prev_id != 0xFFFFFFFFFFFFFFFF:
        if folderNames[prev_id] != "":
            name = folderNames[prev_id] + "/" + name
        prev_id = prevIds[prev_id]

    folders.append(name)

    if name != "":
        os.makedirs(name, exist_ok=True)

pos = fbin.tell()

for i in range(num_files):
    name_crc = unpack(endianness + 'I', fbin.read(4))[0]

    if version >= 8:
        next_neighbour_file_id = unpack(endianness + 'Q', fbin.read(8))[0]
        prev_id = unpack(endianness + 'Q', fbin.read(8))[0]
        flags = unpack(endianness + 'I', fbin.read(4))[0]
        name_offset = unpack(endianness + 'Q', fbin.read(8))[0]
    else:
        next_neighbour_file_id = unpack(endianness + 'I', fbin.read(4))[0]
        prev_id = unpack(endianness + 'I', fbin.read(4))[0]
        flags = unpack(endianness + 'I', fbin.read(4))[0]
        name_offset = unpack(endianness + 'I', fbin.read(4))[0]

    offset = unpack(endianness + 'Q', fbin.read(8))[0]
    size = unpack(endianness + 'Q', fbin.read(8))[0]
    file_data_crc = unpack('<I', fbin.read(4))[0]

    name = get_name(fbin, name_offset)
    full_name = folders[prev_id] + "/" + name

    if version >= 7:
        writetime = unpack(endianness + "Q", fbin.read(8))[0]

        dt = datetime.datetime.utcfromtimestamp((writetime - 116444736000000000) / 10000000)
        print(dt)


    nf = open(full_name, "wb")

    frmdp.seek(offset)
    data = frmdp.read(size)

    if zlib.crc32(bytearray(name.lower(), "ascii")) != name_crc:
        raise Exception("Invalid file name crc checksum")

    if zlib.crc32(data) != file_data_crc:
        raise Exception("Invalid file data crc checksum")

    nf.write(data)
    nf.close()


