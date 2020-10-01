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

fbytecode = open(sys.argv[1], "rb")
fbytecodeparams = open(sys.argv[2], "rb")

# Read strings from dp_bytecodeparameters
#
numValues = unpack("I",  fbytecodeparams.read(4))[0]
numReferences = unpack("I",  fbytecodeparams.read(4))[0]
numStrings = unpack("I", fbytecodeparams.read(4))[0]
dataSize = unpack("I", fbytecodeparams.read(4))[0]

fbytecodeparams.seek(12, 1)

string_offsets = []
for i in range(numStrings):
    string_offsets.append(unpack("I", fbytecodeparams.read(4))[0])

strings = {}
for encoffset in string_offsets:
    overlap = (encoffset & 0x80) != 0

    offset = encoffset >> 8
    offset *= 8
    if overlap:
        offset += 4

    fbytecodeparams.seek(-dataSize + offset, 2)

    string = ""
    c = unpack('c', fbytecodeparams.read(1))[0].decode('ascii')
    while c != '\0':
        string += c
        c = unpack('c', fbytecodeparams.read(1))[0].decode('ascii')

    string.replace("\"", "'")

    strings[encoffset] = string

# Read the actual bytecode in dp_bytecode.bin
#
numValues = unpack("I",  fbytecode.read(4))[0]
numReferences = unpack("I",  fbytecode.read(4))[0]
numStrings = unpack("I", fbytecode.read(4))[0]
dataSize = unpack("I", fbytecode.read(4))[0]

fbytecode.seek(12, 1)

references = []

for i in range(numReferences):
    reference = unpack("I", fbytecode.read(4))[0]
    references.append(reference)

code_start = fbytecode.tell()
section_started = False

f = open("bytecode.txt", "w")

while fbytecode.tell() < dataSize + code_start:
    opcode = unpack("I", fbytecode.read(4))[0]

    if opcode == 0xFFFFFFFF:
        if section_started:
            section_started = False
        continue
    elif not section_started:
        section_started = True
        f.write("# ----------------------------\n")
        f.write("# Code start at " + hex(int((fbytecode.tell() - code_start) / 8)) + "\n")

    op = (opcode & 0xFF000000) >> 24
    param1 = (opcode & 0xFF0000) >> 16
    param2 = (opcode & 0xFF00) >> 8
    param3 = opcode & 0xFF

    if op == 1: # push
        string = False
        if fbytecode.tell() - code_start in references:
            string = True
        value = unpack("I", fbytecode.read(4))[0]
        if string:
            value = "\"" + strings[value] + "\""
        f.write("push " + str(value) + "\n")
    elif op == 2: # push_gid
        group = unpack("I", fbytecode.read(4))[0]
        id = unpack("I", fbytecode.read(4))[0]
        f.write("push_gid " + str(group) + " " + str(id) + "\n")
    elif op == 3: # call_global
        f.write("call_global num_args=" + str(param3) + " ret_type=" + str(param2) + "\n")
    elif op == 4: # call_object
        f.write("call_object num_args=" + str(param3) + " ret_type=" + str(param2) + "\n")
    elif op == 13: # ret
        f.write("ret\n")
    elif op == 14: # int_to_float
        f.write("int_to_float\n")
    elif op == 15:  # set_member_by_id
        f.write("set_member_by_id id=" + str(param3) + "\n")
    elif op == 16: # get_member_by_id
        f.write("get_member_by_id id=" + str(param3) + "\n")
    elif op == 19: # cmp
        f.write("cmp\n")
    elif op == 21: # unconditional jmp
        offset = unpack("I", fbytecode.read(4))[0]
        f.write("jmp " + str(offset) + "\n")
    elif op == 26: # jmp_if
        offset = unpack("I", fbytecode.read(4))[0]
        f.write("jmp_if " + str(offset) + "\n")
    elif op == 36: # neg
        f.write("neg\n")
    else:
        f.write("unk " + hex(op) + " \n")

f.close()