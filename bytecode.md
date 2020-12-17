Alan Wake VM
============

This document lists every supposed information about Alan Wakes script byte code which is used to control the
logic of the scene. It seems to be a regular stack based vm bytecode.

Commands
------

Every command is at least 4 bytes long where last byte denotes the opcode.

Opcode | Command
-------|-------
0x01   | push
0x02   | push_gid
0x03   | call_global
0x04   | call_object
0x05   | mul_float (?)
0x09   | mul_int (?)
0x0b   | ??
0x0c   | ?? (Some comparison?)
0x0d   | ret
0x0e   | int_to_float
0x0f   | set_member_by_id (?)
0x10   | get_member_by_id (?)
0x13   | cmp
0x15   | jmp
0x1a   | jmp_if
0x1c   | and
0x1d   | or
0x1e   | not
0x20   | ??
0x23   | ??
0x24   | neg (?) (bool_to_int??)
0x25   | ??

* get_member
  * get a member of the called object
  * First byte denotes the type of the variable
    * 1 -> string
    * 2 -> float
    * 3 -> boolean
  * Push this member to the stack

* push
  * Data 4 byte is appended

* push_gid
  * Appended is a 4 byte gid type (?) and a 4 byte gid associated with an entry in the GIDRegistry.txt files
  * push this gid to the stack

* call_global
  * pops object name from stack
  * pops method name from stack
  * pops as many arguments from stack as given in the first byte
  * execute method
  * pushs a return value with the type specified by the second byte or nothing if this byte is zero

* call_object
  * pops object from stack
  * pops method name from stack
  * pops as many arguments from stack as given in the first byte
  * execute method
  * Probably return values?

* int_to_float
  * pops integer from stack
  * pushs to float converted integer to stack
  
* cmp
  * pops two integers from the stack
  * pushs 1 to the stack if they are equal or 0 if they are not

* jmp (unconditional)
  * appended is a 4 byte offset
  * seek over the offset

* jmp_if
  * appended is a 4 byte offset
  * pops integer from stack
  * if it is not zero seek over the offset

API
---

A (kind of) reference for the scripting API of Alan Wake can be found in the file messages/messages.xml file
which explains all possible commands.

```
push_gid sourcedata\sounds\ambience\oneshot_generic_close_rattle_snake
push PlaySound
push this
call args=2 ret=none
unk 0x0d
push_gid #scene1_reststop::_misc::scene1_audio::prefab::ambient_rattlesnake_trigger_004::prefab::PublicInterface
unk 0x10 0x35
push 1
unk 0x13
unk 0x24
push 1
unk 0x13
unk 0x1A 17?
push_gid push_gid #scene1_reststop::_misc::scene1_audio::prefab::ambient_rattlesnake_trigger_004::prefab::PublicInterface
unk 0x10 0x37
push_gid push_gid #scene1_reststop::_misc::scene1_audio::prefab::ambient_rattlesnake_trigger_004::prefab::PublicInterface
unk 0x10 0x36
push_gid push_gid #scene1_reststop::_misc::scene1_audio::prefab::ambient_rattlesnake_trigger_004::prefab::PublicInterface
unk 0x10 0x38
push StartTimer
push this
call args=3
push 0
push EnableTrigger
push this
call args=1
unk 0x0d
push 1
push EnableTrigger
push this
call args=1
unk 0x0d
push 1
push_gid push_gid #scene1_reststop::_misc::scene1_audio::prefab::ambient_rattlesnake_trigger_004::prefab::PublicInterface
unk 0x0f 0x35
unk 0x0d
```

```asm
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 11
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 12
push GetRand
push GAME
call_global args=2 ret=float
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x0F 10
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 8
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 7
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 9
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 10
push StartTimerWithDuration
push this
call_global args=4 ret=none
unk 0x0d
push 0.5f
push FadeIn
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01::snd_small_animal_scurry_loop
call_object args=1 ret=none
unk 0x0d
push 0.5f
push FadeOut
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01::snd_small_animal_scurry_loop
call_object args=1 ret=none
unk 0x0d
push 0.5f
push FadeIn
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01::snd_small_animal_scurry_loop
call_object args=1 ret=none
unk 0x0d
push 0.5f
push FadeOut
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01::snd_small_animal_scurry_loop
call_object args=1 ret=none
unk 0x0d
push RandomInterval
push SendCustomEvent
push this
call args=1 ret=none
unk 0x0d
push RandomInterval
push SendCustomEvent
push this
call args=1 ret=none
unk 0x0d
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 11
push_gid #scene1_reststop::_misc::scene1_audio::prefab::scene1_cave_insects_scurrying_000::prefab::Insects01
unk 0x10 12
push GetRand
push GAME
call_global args=2 ret=float
```
