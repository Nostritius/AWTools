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
import io
import copy

from struct import unpack, pack

class Format(enum.Enum):
    RGBA8_LUT = 0
    RGBA_DXT1 = 5
    RGBA8 = 6
    RGBA_DXT3 = 7
    RGBA_DXT5 = 9

class Color:
    r = 0
    g = 0
    b = 0
    a = 0

def write_tga(image_data, width, height, pixel_depth, file):
    tga = open(file, "wb")

    tga.write(pack('B', 0))  # Image ID Length
    tga.write(pack('B', 0))  # Color Map Type
    tga.write(pack('B', 2))  # Image type

    # Color Map specification
    tga.write(pack('H', 0))  # First Entry Index
    tga.write(pack('H', 0))  # Color Map Length
    tga.write(pack('B', 0))  # Color Map Entry size

    # Image specification
    tga.write(pack('H', 0))  # X-origin
    tga.write(pack('H', 0))  # Y-origin
    tga.write(pack('H', width))  # Image width
    tga.write(pack('H', height))  # Image height
    tga.write(pack('B', pixel_depth))  # Pixel depth
    tga.write(pack('B', 0))  # image descriptor

    tga.write(image_data)

def decode565(x):
    rgba = Color()
    rgba.r = (x & 0xf800) >> 8
    rgba.r |= rgba.r >> 5
    rgba.g = (x & 0x7e0) >> 3
    rgba.g |= rgba.g >> 6
    rgba.b = (x & 0x1f) << 3
    rgba.b |= rgba.b >> 5
    rgba.a = 0xFF

    return copy.copy(rgba)

def decompressDXT1(compressed_image_data, width, height):
    d = io.BytesIO(compressed_image_data)

    image_colors = [None] * int(width * height)

    for y in range(height - 4, -4, -4):
        for x in range(0, width, 4):
            color_0 = unpack('H', d.read(2))[0]
            color_1 = unpack('H', d.read(2))[0]
            pixels = unpack('>I', d.read(4))[0]

            c1 = decode565(color_0)
            c2 = decode565(color_1)

            table = []
            table.append(copy.copy(c1))
            table.append(copy.copy(c2))

            if color_0 > color_1:
                c3 = Color()
                c3.r = int((2 * c1.r + c2.r) / 3) % 256
                c3.g = int((2 * c1.g + c2.g) / 3) % 256
                c3.b = int((2 * c1.b + c2.b) / 3) % 256
                c3.a = 0xff
                c4 = Color()
                c4.r = int((c1.r + 2 * c2.r) / 3) % 256
                c4.g = int((c1.g + 2 * c2.g) / 3) % 256
                c4.b = int((c1.b + 2 * c2.b) / 3) % 256
                c4.a = 0xff
            else:
                c3 = Color()
                c3.r = int((c1.r + c2.r) / 2) % 256
                c3.g = int((c1.g + c2.g) / 2) % 256
                c3.b = int((c1.b + c2.b) / 2) % 256
                c3.a = 0xff
                c4 = Color()
                c4.r = 0
                c4.g = 0
                c4.b = 0
                c4.a = 0

            table.append(copy.copy(c3))
            table.append(copy.copy(c4))

            for i in range(16):
                index = 3 & (pixels >> (2 * i))
                image_colors[(x + i % 4) + (y + int(i / 4)) * width] = copy.copy(table[index])

    d = io.BytesIO()

    for color in image_colors:
        d.write(pack('B', color.r))
        d.write(pack('B', color.g))
        d.write(pack('B', color.b))
        d.write(pack('B', color.a))

    image_data = d.getbuffer()

    return image_data

def decompressDXT3(compressed_image_data, width, height):
    d = io.BytesIO(compressed_image_data)

    image_colors = [None] * int(width * height)

    for y in range(height - 4, -4, -4):
        for x in range(0, width, 4):
            alphas = unpack('4H', d.read(8))
            color_0 = unpack('H', d.read(2))[0]
            color_1 = unpack('H', d.read(2))[0]
            pixels = unpack('>I', d.read(4))[0]

            c1 = decode565(color_0)
            c2 = decode565(color_1)

            table = []
            table.append(copy.copy(c1))
            table.append(copy.copy(c2))

            c3 = Color()
            c3.r = int((2 * c1.r + c2.r) / 3) % 256
            c3.g = int((2 * c1.g + c2.g) / 3) % 256
            c3.b = int((2 * c1.b + c2.b) / 3) % 256
            c3.a = 0xff
            c4 = Color()
            c4.r = int((c1.r + 2 * c2.r) / 3) % 256
            c4.g = int((c1.g + 2 * c2.g) / 3) % 256
            c4.b = int((c1.b + 2 * c2.b) / 3) % 256
            c4.a = 0xff

            table.append(copy.copy(c3))
            table.append(copy.copy(c4))

            for i in range(16):
                index = 3 & (pixels >> (2 * i))

                alpha = (alphas[int(i / 4)] >> (i % 4)) & 0xF

                c = copy.copy(table[index])
                c.a = alpha << 4
                image_colors[(x + i % 4) + (y + int(i / 4)) * width] = c

    d = io.BytesIO()

    for color in image_colors:
        d.write(pack('B', color.a))
        d.write(pack('B', color.r))
        d.write(pack('B', color.g))
        d.write(pack('B', color.b))

    image_data = d.getbuffer()

    return image_data


f = open(sys.argv[1], "rb")

type = unpack('I', f.read(4))[0]
format = Format(unpack('I', f.read(4))[0])
width = unpack('I', f.read(4))[0]
height = unpack('I', f.read(4))[0]
depth = unpack('I', f.read(4))[0]  # Not pixel depth, but rather depth in 3 dimensional textures
mipmap_count = unpack('I', f.read(4))[0]
filter = unpack('I', f.read(4))[0]

f.seek(4, 1) # Not even mentioned in the meta files, so probably reserved?

if type == 2:
    d = io.BytesIO()
    for i in range(6):
        d.write(f.read(width * height * 4))

    image_data = d.getbuffer()
    height *= 6
else:
    image_data = f.read(width * height * 4)

if format == Format.RGBA_DXT1:
    image_data = decompressDXT1(image_data, width, height)
elif format == Format.RGBA_DXT3:
    image_data = decompressDXT3(image_data, width, height)

write_tga(image_data, width, height, 32, sys.argv[1] + ".tga")
