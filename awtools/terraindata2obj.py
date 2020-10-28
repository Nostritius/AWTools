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

version = unpack('I', f.read(4))[0]
no_tile_names = unpack('?', f.read(1))[0]

obj = open("terraindata.obj", "w")
mtl = open("terraindata.mtl", "w")

positions = []
normals = []
indices = []

if not no_tile_names:
    num_tile_files = unpack('I', f.read(4))[0]
    for i in range(num_tile_files):
        tile_file_name_length = unpack('I', f.read(4))[0]
        tile_file_name = unpack('<' + str(tile_file_name_length) + 's', f.read(tile_file_name_length))[0].decode('ascii')
        tile_file_name.replace('\0', '')
        print(tile_file_name)

    # ??
    num_indices = unpack('I', f.read(4))[0]
    for i in range(num_indices):
        f.seek(2*6, 1)

    # Vertices
    num_vertices = unpack('I', f.read(4))[0]
    for i in range(num_vertices):
        positions.append(unpack("fff", f.read(12)))
        nx, ny, nz = unpack('hhh', f.read(6))
        normals.append((nx / 32767.0, ny / 32767.0, nz / 32767.0))
        f.seek(2, 1)

    # Polygons
    num_polygons = unpack('I', f.read(4))[0]
    for i in range(num_polygons):
        vertex_references = unpack('iiii', f.read(16))
        indices.append(vertex_references)

        characters = []
        numVertexReferences = unpack('B', f.read(1))[0]
        for j in range(3):
            characters.append(unpack('B', f.read(1))[0])

        f.seek(0x40 + 0x48, 1)

        x, y, z = unpack('fff', f.read(12))
        radius = unpack('f', f.read(4))[0]

        #obj.write("v " + str(x) + " " + str(y)  + " " + str(z) + "\n")

        polygon_references = unpack('HHHH', f.read(8))

        values3 = []
        for j in range(4):
            values3.append(unpack('B', f.read(1))[0])

        val1 = unpack('H', f.read(2))
        val2 = unpack('H', f.read(2))
        val3 = unpack('I', f.read(4))
        f.seek(4, 1)

else:
    poly_count = unpack('I', f.read(4))[0]
    for i in range(poly_count):
        f.seek(16)

# Color blending maps
num_color_blends = unpack('I', f.read(4))[0]
for i in range(num_color_blends):
    id = unpack('I', f.read(4))[0]
    length = unpack('I', f.read(4))[0]

    pgm = open('blend_' + str(id) + '.pgm', 'w')
    pgm.write("P2\n" + str(length) + " " + str(length) + "\n")
    pgm.write("65535\n")
    for x in range(length):
        for y in range(length):
            pgm.write(str(unpack('H', f.read(2))[0]) + " ")
        pgm.write('\n')

# Normal Blending maps
num_unknown4 = unpack('I', f.read(4))[0]
for i in range(num_unknown4):
    id = unpack('I', f.read(4))[0]
    length = unpack('I', f.read(4))[0]

    pgm = open('blend2_' + str(id) + '.pgm', 'w')
    pgm.write("P2\n" + str(length) + " " + str(length) + "\n")
    pgm.write("65535\n")
    for x in range(length):
        for y in range(length):
            pgm.write(str(unpack('H', f.read(2))[0]) + " ")
        pgm.write('\n')

# Write material
for i in range(num_color_blends):
    mtl.write("newmtl color_blend_%d\n" % i)
    mtl.write("Ka 1.0 1.0 1.0\n")
    #mtl.write("Kd 1.0 1.0 1.0\n")
    mtl.write("illum 1\n")
    mtl.write("map_Kd blend_%i.pgm\n" % i)

# Write obj mesh
obj.write("mtllib terraindata.mtl\n")

for i in range(len(positions)):
    obj.write("v %f %f %f\n" % positions[i])

for i in range(len(normals)):
    obj.write("vn %f %f %f\n" % normals[i])

for i in range(len(indices)):
    #if -1 in indices[i]:
    #    continue

    obj.write("usemtl color_blend_%d\n" % i)

    index1 = list(indices[i][0:3])
    if -1 in index1:
        continue
    index1[0] += 1
    index1[1] += 1
    index1[2] += 1
    index1 = tuple(index1)
    obj.write("f %d %d %d\n" % index1)

    index2 = list(indices[i][1:4])
    if -1 in index2:
        continue
    index2[0] = index1[0]
    index2[1] += 1
    index2[2] += 1
    index2 = tuple(index2)
    obj.write("f %d %d %d\n" % index2)