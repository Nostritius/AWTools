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

import os
import sys

from struct import unpack, pack


fdds = open(sys.argv[1], "rb")
ftex = open(os.path.splitext(sys.argv[1])[0] + ".tex", "wb")

dds_magic = unpack("<4s", fdds.read(4))[0].decode("ascii")
if dds_magic != "DDS ":
    raise Exception("Invalid dds file")

fdds.seek(4, 1)  # Header Size
flags = unpack("I", fdds.read(4))[0]
has_mipmaps = (flags & 0x20000) != 0
has_depth = (flags & 0x800000) != 0

height = unpack("I", fdds.read(4))[0]
width = unpack("I", fdds.read(4))[0]

fdds.seek(4, 1)  # Pitch or linear size

depth = unpack("I", fdds.read(4))[0]
if not has_depth:
    depth = 1
mipmap_count = unpack("I", fdds.read(4))[0]
if not has_mipmaps:
    mipmap_count = 1

fdds.seek(44, 1)  # Reserved

# Pixel Format
fdds.seek(4, 1)  # Size

flags = unpack("I", fdds.read(4))[0]
has_fourcc = (flags & 0x4) != 0
if not has_fourcc:
    raise Exception("Only compressed textures supported by now")

fourcc = unpack("<4s", fdds.read(4))[0].decode("ascii")
fdds.seek(20, 1)

# More caps
fdds.seek(8, 1)

fdds.seek(12, 1)  # Reserved

image_data = fdds.read()

# Write tex file
ftex.write(pack("I", 0))

if fourcc == "DXT1":
    format = 5
elif fourcc == "DXT3":
    format = 7
elif fourcc == "DXT5":
    format = 9
else:
    raise Exception("Unsupported texture format")
ftex.write(pack("I", format))
ftex.write(pack("I", width))
ftex.write(pack("I", height))
ftex.write(pack("I", depth))
ftex.write(pack("I", mipmap_count))
ftex.write(pack("I", 0))  # Filter
ftex.write(pack("I", 0))

ftex.write(image_data)
