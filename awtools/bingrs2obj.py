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
from struct import unpack

f = open(sys.argv[1], "rb")

version = unpack("I", f.read(4))[0]
if version != 3:
    raise Exception("Invalid version")

mesh_count = unpack('I', f.read(4))[0]
num_vertices = unpack('I', f.read(4))[0]
num_indices = unpack('I', f.read(4))[0]

# Uniforms
num_uniforms = unpack('I', f.read(4))[0]
for i in range(num_uniforms):
    name_length = unpack('I', f.read(4))[0]
    name = unpack('<' + str(name_length) + 's', f.read(name_length))[0].decode('ascii')

    uniform_type = unpack('I', f.read(4))[0]

    if uniform_type == 7:
        texture_name_length = unpack('I', f.read(4))[0]
        texture_name = unpack('<' + str(texture_name_length) + 's', f.read(texture_name_length))[0].decode('ascii')
    else:
        # Both Alan Wake and Alan Wakes American nightmare only have one color map sampler
        raise Exception("")

fobj = open(os.path.splitext(sys.argv[1])[0] + ".obj", "w")

# Meshes
for i in range(mesh_count):
    num_mesh_vertices = unpack('I', f.read(4))[0]
    num_mesh_indices = unpack('I', f.read(4))[0]

    fobj.write("o grass_" + str(i) + "\n")

    for j in range(num_mesh_vertices):
        position = unpack('fff', f.read(12))
        fobj.write("v %f %f %f\n" % position)
        unk1 = unpack('bbbb', f.read(4))

    fobj.write("s off\n")

    for j in range(0, num_mesh_indices, 3):
        face = list(unpack('HHH', f.read(6)))
        face[0] += 1
        face[1] += 1
        face[2] += 1

        fobj.write("f %d %d %d\n" % tuple(face))

fobj.close()