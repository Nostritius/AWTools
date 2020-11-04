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

f = open(sys.argv[1], "rb")

magic = unpack('<4s', f.read(4))[0].decode('ascii')
table_offset = unpack('I', f.read(4))[0]

f.seek(-table_offset, 2)

num_files = unpack('I', f.read(4))[0]
offset = 8

for i in range(num_files):
    file_size = unpack('I', f.read(4))[0]
    name_length = unpack('I', f.read(4))[0]
    name = unpack('<' + str(name_length) + 's', f.read(name_length))[0].decode('ascii')
    last_pos = f.tell()
    f.seek(offset)
    fout = open(name, "wb")
    fout.write(f.read(file_size))
    fout.close()
    f.seek(last_pos)
    offset += file_size