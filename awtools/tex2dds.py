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
import enum
import math

from struct import unpack, pack


class Format(enum.Enum):
    RGBA8_LUT = 0
    GRAYSCALE_4BIT = 1  # Potentially swizzled?
    RGBA_CUBE_DXT1 = 4
    RGBA_DXT1 = 5
    RGBA8 = 6
    RGBA_DXT3 = 7
    RGBA_DXT5 = 9
    RGBA8_CUBE = 11


f = open(sys.argv[1], "rb")

type = unpack('I', f.read(4))[0]
format = Format(unpack('I', f.read(4))[0])
width = unpack('I', f.read(4))[0]
height = unpack('I', f.read(4))[0]
depth = unpack('I', f.read(4))[0]  # Not pixel depth, but rather depth in 3 dimensional textures
mipmap_count = unpack('I', f.read(4))[0]
filter = unpack('I', f.read(4))[0]

f.seek(0x20)

image_data = f.read()
f.close()

dds_filename = os.path.splitext(sys.argv[1])[0] + ".dds"
f = open(dds_filename, "wb")

f.write(pack('<4s', bytearray("DDS ", "ascii")))  # DDS Magic bytes
f.write(pack('I', 124))

flags = 0x1 | 0x2 | 0x4 | 0x1000

# Is Depth texture?
if type == 1:
    flags |= 0x800000

# Has Mipmaps?
if mipmap_count > 1:
    flags |= 0x20000

if format == Format.RGBA_DXT1 or format == Format.RGBA_DXT3 or Format.RGBA_DXT5:
    flags |= 0x80000

f.write(pack('I', flags))
f.write(pack('I', height))
f.write(pack('I', width))

if format == Format.RGBA_DXT1:
    image_size = max(math.ceil(width / 4) * math.ceil(height / 4) * 8, 8)
elif format == Format.RGBA_DXT3 or format == Format.RGBA_DXT5:
    image_size = max(math.ceil(width / 4) * math.ceil(height / 4) * 16, 16)

f.write(pack('I', image_size))

f.write(pack('I', depth))
f.write(pack('I', mipmap_count))

for i in range(11):
    f.write(pack('I', 0))

f.write(pack('I', 32))
pf_flags = 0
if type == 5 or type == 7 or type == 9:
    pf_flags |= 0x4

f.write(pack('I', pf_flags))

if format == Format.RGBA_DXT1:
    f.write(pack('<4s', bytearray("DXT1", "ascii")))
elif format == Format.RGBA_DXT3:
    f.write(pack('<4s', bytearray("DXT3", "ascii")))
elif format == Format.RGBA_DXT5:
    f.write(pack('<4s', bytearray("DXT5", "ascii")))
else:
    f.write(pack('<4s', bytearray("    ", "ascii")))

f.write(pack("I", 0))
f.write(pack("I", 0))
f.write(pack("I", 0))
f.write(pack("I", 0))
f.write(pack("I", 0))

dds_caps = 0x1000
if mipmap_count > 1:
    dds_caps |= 0x400000

if mipmap_count > 1 or depth > 1 or type != 0:
    dds_caps |= 0x8

f.write(pack("I", dds_caps))

dds_caps2 = 0
if type == 2:
    dds_caps2 |= 0x200 | 0x400 | 0x800 | 0x1000 | 0x2000 | 0x4000 | 0x8000
elif type == 1:
    dds_caps2 |= 0x200000

f.write(image_data)

# Reserved Caps
f.write(pack("I", 0))
f.write(pack("I", 0))

# Reserved
f.write(pack("I", 0))

f.write(image_data)
