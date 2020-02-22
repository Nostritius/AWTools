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

from struct import unpack

f = open(sys.argv[1], "rb")

magic_string = unpack("<4s", f.read(4))[0].decode("ascii")

if magic_string != "RFX ":
    raise Exception("Invalid magic string")

unknown1 = unpack('I', f.read(4))[0]
numStrings = unpack('I', f.read(4))[0]

for i in range(numStrings):
    nameLength = unpack('I', f.read(4))[0]
    name = unpack("<" + str(nameLength) + "s", f.read(nameLength))[0].decode("ascii")

    f.seek(4, 1)

numPrograms = unpack('I', f.read(4))[0]

for i in range(numPrograms):
    nameLength = unpack('I', f.read(4))[0]
    name = unpack("<" + str(nameLength) + "s", f.read(nameLength))[0].decode("ascii")

    numShaders = unpack('I', f.read(4))[0]
    f.seek(4, 1)  # Probably numShaders is intended to be 64 bit?

    for j in range(numShaders * 2):
        fileSize = unpack('I', f.read(4))[0]

        fxo = open(os.path.splitext(sys.argv[1])[0] + "_" + name + "_" + str(j) + ".fxo", "wb")

        fxo.write(f.read(fileSize))
        fxo.close()

