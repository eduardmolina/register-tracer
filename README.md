# Python Register Tracer

Loading this dump and tracking `rbx`:

```
00007FF632E8CEB9  lea r8, [0x00007FF6317146CB]
00007FF632E8CEC0  add rbx, rax
00007FF632E8CEC3  not rdx
00007FF632E8CEC6  mov rax, rbx
00007FF632E8CEC9  shr rax, 0x0E
00007FF632E8CECD  xor rbx, rax
00007FF632E8CED0  mov rax, rbx
00007FF632E8CED3  shr rax, 0x1C
00007FF632E8CED7  xor rbx, rax
00007FF632E8CEDA  lea rax, [0x00007FF63171099B]
00007FF632E8CEE1  sub rcx, rax
00007FF632E8CEE4  mov rax, rbx
```

This tool will generate the path that really changes `rbx` value removing all obfuscated code:

```
00007FF632E8CEC0  add rbx, rax
00007FF632E8CEC6  mov rax, rbx
00007FF632E8CEC9  shr rax, 0x0E
00007FF632E8CECD  xor rbx, rax
00007FF632E8CED0  mov rax, rbx
00007FF632E8CED3  shr rax, 0x1C
00007FF632E8CED7  xor rbx, rax
```
