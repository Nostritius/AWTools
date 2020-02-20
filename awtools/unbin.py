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
import zlib

from struct import unpack

f = open(sys.argv[1], "rb")

num_files = unpack('I', f.read(4))[0]

entries = []
for i in range(num_files):
    file_name_length = unpack('I', f.read(4))[0]
    file_name = unpack("<" + str(file_name_length) + "s", f.read(file_name_length))[0].decode('ASCII')
    length = unpack('I', f.read(4))[0]

    entries.append({"file_name": file_name, "length": length})

compressed_data = f.read()

data = zlib.decompress(compressed_data)

current_index = 0
for entry in entries:
    file_name = entry["file_name"]
    length = entry["length"]

    ef = open(file_name, "wb")
    ef.write(data[current_index:current_index + length])
    current_index += length

    print(file_name)
