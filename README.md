Alan Wake Tools
===============

This repository adds multiple python tools for extracting data from the games Alan Wake and Alan Wakes American 
Nightmare. It is mainly intended for experimenting and reverse engineering several file formats, which are not yet 
fully understood. The file formats mainly consist of structural data, like description of levels or save games.

The following tools are available:

* unrmdp.py unpack rmdp/bin archive structures
* unbin.py unpack bin or resources archives
* unobj.py unpack obj shader archives
* rmdp.py pack rmdp/bin archive structures
* bin.py pack bin or resources archives
* tex2tga convert tex texture to a tga image
* bin2xml.py translate a binary data file to a readable xml file
* binfnt2xml.py translate a binfnt file to a readable xml file and extract the font texture
* packmeta2xml.py translate a packmeta file to a readable xml file
* collisions2obj.py convert a collisions mesh to a Wavefront mesh file
* string_table2xml.py convert a string table file to a readable xml file
* xml2string_table.py pack a string table back together
* roadmap2xml.py translate a cid_roadmap.bin file to a readable xml file
* disasm.py disassembles bytecode given by dp_bytecode.bin and dp_bytecodeparams.bin
* dp2xml.py convert a dp file to xml

The tools are currently mostly tested against Alan Wakes American Nightmare. While some of them like unrmdp or unbin
also work with the original Alan Wake.

Furthermore the file bytecode.md contains some information about the bytecode used by Alan Wake