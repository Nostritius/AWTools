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
import os.path
import zlib
import copy

from struct import pack


class FileEntry:
    path = ""
    name = ""
    size = 0


f = open(sys.argv[1], "wb")
folder = sys.argv[2]

files = []
for file in os.listdir(folder):
    if not os.path.isfile(folder + "/" + file):
        continue

    entry = FileEntry()
    entry.name = file
    entry.path = folder + "/" + file
    entry.size = os.path.getsize(folder + "/" + file)

    files.append(copy.copy(entry))

f.write(pack('I', len(files)))

data = bytearray()

for entry in files:
    f.write(pack('I', len(entry.name)))
    f.write(bytearray(entry.name, "ascii"))
    f.write(pack('I', entry.size))

    data += open(entry.path, "rb").read()

f.write(zlib.compress(data))
f.close()
