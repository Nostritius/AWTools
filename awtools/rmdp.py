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

from struct import pack

folder = sys.argv[1]

fbin = open(sys.argv[2], "wb")
frmdp = open(sys.argv[3], "wb")

file_id = 0
folder_id = 0

folder_entries = []
file_entries = []
name_entries = {}
names = []

class FolderEntry:
    name = ""
    path = ""
    id = 0
    prev_folder = 0xFFFFFFFF
    next_neighbour_folder = 0xFFFFFFFF
    next_lower_folder = 0xFFFFFFFF
    next_file = 0xFFFFFFFF


class FileEntry:
    name = ""
    path = ""
    id = 0
    folder = 0
    prev_folder = 0xFFFFFFFF
    next_file = 0xFFFFFFFF


def index_folder(parent, folder):
    global folder_id
    global file_id

    if parent.path == "":
        path = folder
    else:
        path = parent.path + "/" + folder

    folder_entry = FolderEntry()
    folder_entry.name = folder
    folder_entry.path = path
    folder_entry.id = folder_id
    folder_entry.prev_folder = parent.id

    names.append(folder_entry.name)

    folder_id += 1

    if parent.next_lower_folder == 0xFFFFFFFF:
        parent.next_lower_folder = folder_entry.id

    last_file_entry = None
    last_folder_entry = None

    next_file_id = file_id

    for entry in os.listdir(folder_entry.path):
        if os.path.isdir(path + "/" + entry):
            print(path + "/" + entry)
            lower_folder_entry = index_folder(folder_entry, entry)
            if last_folder_entry == None:
                folder_entry.next_lower_folder = lower_folder_entry.id
            else:
                last_folder_entry.next_neighbour_folder = lower_folder_entry.id
            last_folder_entry = lower_folder_entry
        elif os.path.isfile(path + "/" + entry):
            file = FileEntry()
            file.name = entry
            file.path = path + "/" + entry
            file.prev_folder = folder_entry.id
            file.id = file_id

            print(file.path)

            names.append(entry)

            file_id += 1

            if last_file_entry == None:
                folder_entry.next_file = file.id
            else:
                last_file_entry.next_file = file.id

            last_file_entry = file

            file_entries.append(file)


    folder_entries.append(folder_entry)

    return folder_entry

root_entry = FolderEntry()
root_entry.id = folder_id
folder_entries.append(root_entry)

folder_id += 1

index_folder(root_entry, folder)

fbin.write(pack('B', 0))

fbin.write(pack('I', 7))

fbin.write(pack('I', len(folder_entries)))
fbin.write(pack('I', len(file_entries)))

fbin.write(pack('Q', 1))

name_size = 0
name_list = []

for name in names:
    if name not in name_entries:
        name_entries[name] = name_size
        name_size += len(name) + 1
        name_list.append(name)

fbin.write(pack('I', name_size))
fbin.write(pack('<7s', bytearray("d:\data", "ascii")))

for i in range(121):
    fbin.write(pack('B', 0))

folder_entries.sort(key=lambda f: f.id)
file_entries.sort(key=lambda f: f.id)

for folder in folder_entries:
    print(folder.id)

    fbin.write(pack('I', zlib.crc32(bytearray(folder.name, "ascii"))))
    fbin.write(pack('I', folder.next_neighbour_folder))
    fbin.write(pack('I', folder.prev_folder))
    fbin.write(pack('I', 0))

    if folder.name != "":
        fbin.write(pack('I', name_entries[folder.name]))
    else:
        fbin.write(pack('I', 0xFFFFFFFF))

    fbin.write(pack('I', folder.next_lower_folder))
    fbin.write(pack('I', folder.next_file))

for file in file_entries:
    fbin.write(pack('I', zlib.crc32(bytearray(file.name, "ascii"))))
    fbin.write(pack('I', file.next_file))
    fbin.write(pack('I', file.prev_folder))
    fbin.write(pack('I', 0))
    fbin.write(pack('I', name_entries[file.name]))

    f = open(file.path, "rb")
    data = f.read()

    fbin.write(pack('Q', frmdp.tell()))
    fbin.write(pack('Q', len(data)))

    fbin.write(pack('I', zlib.crc32(data)))

    frmdp.write(data)

    fbin.write(pack('Q', 0))

fbin.write(pack('I', 0))
fbin.write(pack('I', 0xFFFFFFFF))
fbin.write(pack('I', 0xFFFFFFFF))
fbin.write(pack('<4s', bytearray("ctor", "ascii")))
fbin.write(pack('I', 0xFFFFFFFF))
fbin.write(pack('I', 0xFFFFFFFF))
fbin.write(pack('I', 0xFFFFFFFF))

for name in name_list:
    fbin.write(pack("<" + str(len(name) + 1) + "s", bytearray(name + "\0", "ascii")))

fbin.close()
frmdp.close()
