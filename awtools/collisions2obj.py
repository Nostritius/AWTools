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

magic_id = unpack('I', f.read(4))[0]
if magic_id != 3:
    raise Exception("Invalid magic id")

num_vertices = unpack('I', f.read(4))[0]
num_indices = unpack('I', f.read(4))[0]

vertices = []
faces = []
face_types = []

for i in range(num_vertices):
    x = unpack('f', f.read(4))[0]
    y = unpack('f', f.read(4))[0]
    z = unpack('f', f.read(4))[0]

    vertices.append((x, y, z))

for i in range(int(num_indices / 3)):
    a = unpack('H', f.read(2))[0] + 1
    b = unpack('H', f.read(2))[0] + 1
    c = unpack('H', f.read(2))[0] + 1

    faces.append((a, b, c))

# Polygon Types?
# Material Types? For Mat dependent sound?
for i in range(int(num_indices / 3)):
    face_types.append(unpack('B', f.read(1))[0])

unknown1 = unpack('I', f.read(4))[0]  # Always 1?

num_vertices_2 = unpack('I', f.read(4))[0]
num_indices_2 = unpack('I', f.read(4))[0]

# TODO: There is much more unknown data in the file

fobj = open(sys.argv[1] + ".obj", "w")

for v in vertices:
    fobj.write("v %f %f %f\n" % v)

for f in faces:
    fobj.write("f %d %d %d\n" % f)

fobj.close()
