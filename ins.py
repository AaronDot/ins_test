import os
import numpy as np

def write(line, file):
    with open("dump_i.S", "r") as input:
        text = input.read()
        with open(file, "w") as output:
            output.write(text.replace("nop\n", line))

def build(line):
    write(line, "tmp.S")
    ret = os.system("gcc -nostdlib -static tmp.S show_i.c -o tmp")
    if ret != 0:
        return ret
    ret = os.system("./tmp > want.txt 2>&1")
    if ret != 0:
        return ret
    #return os.system("/usr/bin/valgrind --tool=none -q ./tmp > out.txt 2>&1")
    return os.system("../valgrind --tool=none -q ./tmp > out.txt 2>&1")


def diff():
    with open("want.txt", "r") as want:
        with open("out.txt", "r") as out:
            lines1 = want.readlines()
            lines2 = out.readlines()
            if len(lines1) != len(lines2):
                print("len1 != len2")
                return False
            for i in range(0, len(lines1)):
                if i == 3 or i == 11 or i == 21:
                    continue
                if lines1[i] != lines2[i]:
                    print("want: " + lines1[i] + "out: " + lines2[i])
                    return False
            return True

def test(name, func, n):
    for _ in range(0, n):
        line = func(name)
        if build(line) != 0:
            print("Build failed!")
            return False
        if not diff():
            return False
    return True


def rand_reg():
    reg = np.random.randint(4, 32, 1, np.int32)
    while reg[0] == 11 or reg[0] == 21:
        reg = np.random.randint(4, 32, 1, np.int32)
    num = np.random.randint(np.iinfo(np.int64).min, np.iinfo(np.int64).max, 1, np.int64)
    return (reg[0], num[0])

def rand_reg_32():
    reg = np.random.randint(4, 32, 1, np.int32)
    while reg[0] == 11 or reg[0] == 21:
        reg = np.random.randint(4, 32, 1, np.int32)
    num = np.random.randint(0, np.iinfo(np.int32).max, 1, np.int32)
    return (reg[0], num[0])

def rand_imm(n, sign):
    min = 0
    max = 1 << n
    if (sign):
        min = -(1 << (n - 1))
        max = 1 << (n - 1)
    imm = np.random.randint(min, max, 1, np.int32)
    return imm[0]

def rand_imm2(n):
    imm = np.random.randint(0, 1 << n, 2, np.int32)
    min = imm[0]
    max = imm[1]
    if imm[1] < min:
        max = imm[0]
        min = imm[1]
    return (min, max)

def rd_rj(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    line += f"{name} $r{rd}, $r{rj}\n"
    return line

def rd_rj_rk(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    rk, v3 = rand_reg()
    line += f"li.d $r{rk}, {v3}\n    "
    line += f"{name} $r{rd}, $r{rj}, $r{rk}\n"
    return line

def rd_rj_rk_32(name):
    line = ""
    rd, v1 = rand_reg_32()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg_32()
    line += f"li.d $r{rj}, {v2}\n    "
    rk, v3 = rand_reg_32()
    line += f"li.d $r{rk}, {v3}\n    "
    line += f"{name} $r{rd}, $r{rj}, $r{rk}\n"
    return line

def rd_rj_si12(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    si12 = rand_imm(12, True)
    line += f"{name} $r{rd}, $r{rj}, {si12}\n"
    return line

def rd_rj_ui12(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    ui12 = rand_imm(12, False)
    line += f"{name} $r{rd}, $r{rj}, {ui12}\n"
    return line

def rd_rj_si16(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    si16 = rand_imm(16, True)
    line += f"{name} $r{rd}, $r{rj}, {si16}\n"
    return line

def rd_rj_ui5(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    ui5 = rand_imm(5, False)
    line += f"{name} $r{rd}, $r{rj}, {ui5}\n"
    return line

def rd_rj_ui6(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    ui6 = rand_imm(6, False)
    line += f"{name} $r{rd}, $r{rj}, {ui6}\n"
    return line

def rd_rj_msbw_lsbw(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    lsbw, msbw = rand_imm2(5)
    line += f"{name} $r{rd}, $r{rj}, {msbw}, {lsbw}\n"
    return line

def rd_rj_msbd_lsbd(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    lsbd, msbd = rand_imm2(6)
    line += f"{name} $r{rd}, $r{rj}, {msbd}, {lsbd}\n"
    return line

def rd_rj_rk_sa2(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    rk, v3 = rand_reg()
    line += f"li.d $r{rk}, {v3}\n    "
    sa2 = rand_imm(2, False)
    line += f"{name} $r{rd}, $r{rj}, $r{rk}, {sa2}\n"
    return line

def rd_rj_rk_sa2_add1(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    rk, v3 = rand_reg()
    line += f"li.d $r{rk}, {v3}\n    "
    sa2 = rand_imm(2, False) + 1
    line += f"{name} $r{rd}, $r{rj}, $r{rk}, {sa2}\n"
    return line

def rd_rj_rk_sa3(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $r{rj}, {v2}\n    "
    rk, v3 = rand_reg()
    line += f"li.d $r{rk}, {v3}\n    "
    sa3 = rand_imm(3, False)
    line += f"{name} $r{rd}, $r{rj}, $r{rk}, {sa3}\n"
    return line

def rd_si20(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $r{rd}, {v1}\n    "
    si20 = rand_imm(20, True)
    line += f"{name} $r{rd}, {si20}\n"
    return line

def vd_vj_vk(name):
    line = ""
    rd, v1 = rand_reg()
    line += f"li.d $rv{vd}, {v1}\n    "
    rj, v2 = rand_reg()
    line += f"li.d $rv{vj}, {v2}\n    "
    rk, v3 = rand_reg()
    line += f"li.d $v{vk}, {v3}\n    "
    line += f"{name} $r{rd}, $r{rj}, $r{rk}\n"
    return line

insts = [
   # { "name": "add.w",      "func": rd_rj_rk            },
   # { "name": "add.d",      "func": rd_rj_rk            },
   # { "name": "sub.w",      "func": rd_rj_rk            },
   # { "name": "sub.d",      "func": rd_rj_rk            },
   # { "name": "slt",        "func": rd_rj_rk            },
   # { "name": "sltu",       "func": rd_rj_rk            },
   # { "name": "slti",       "func": rd_rj_si12          },
   # { "name": "sltui",      "func": rd_rj_si12          },
   # { "name": "nor",        "func": rd_rj_rk            },
   # { "name": "and",        "func": rd_rj_rk            },
   # { "name": "or",         "func": rd_rj_rk            },
   # { "name": "xor",        "func": rd_rj_rk            },
   # { "name": "orn",        "func": rd_rj_rk            },
   # { "name": "andn",       "func": rd_rj_rk            },
   # { "name": "mul.w",      "func": rd_rj_rk            },
   # { "name": "mulh.w",     "func": rd_rj_rk            },
   # { "name": "mulh.wu",    "func": rd_rj_rk            },
   # { "name": "mul.d",      "func": rd_rj_rk            },
   # { "name": "mulh.d",     "func": rd_rj_rk            },
   # { "name": "mulh.du",    "func": rd_rj_rk            },
   # { "name": "mulw.d.w",   "func": rd_rj_rk            },
   # { "name": "mulw.d.wu",  "func": rd_rj_rk            },
   # { "name": "div.w",      "func": rd_rj_rk_32         },
   # { "name": "mod.w",      "func": rd_rj_rk_32         },
   # { "name": "div.wu",     "func": rd_rj_rk_32         },
   # { "name": "mod.wu",     "func": rd_rj_rk_32         },
   # { "name": "div.d",      "func": rd_rj_rk            },
   # { "name": "mod.d",      "func": rd_rj_rk            },
   # { "name": "div.du",     "func": rd_rj_rk            },
   # { "name": "mod.du",     "func": rd_rj_rk            },
   # { "name": "alsl.w",     "func": rd_rj_rk_sa2_add1   },
   # { "name": "alsl.wu",    "func": rd_rj_rk_sa2_add1   },
   # { "name": "alsl.d",     "func": rd_rj_rk_sa2_add1   },
   # { "name": "lu12i.w",    "func": rd_si20             },
   # { "name": "lu32i.d",    "func": rd_si20             },
   # { "name": "lu52i.d",    "func": rd_rj_si12          },
   # { "name": "addi.w",     "func": rd_rj_si12          },
   # { "name": "addi.d",     "func": rd_rj_si12          },
   # { "name": "addu16i.d",  "func": rd_rj_si16          },
   # { "name": "andi",       "func": rd_rj_ui12          },
   # { "name": "ori",        "func": rd_rj_ui12          },
   # { "name": "xori",       "func": rd_rj_ui12          },
   # { "name": "sll.w",      "func": rd_rj_rk            },
   # { "name": "srl.w",      "func": rd_rj_rk            },
   # { "name": "sra.w",      "func": rd_rj_rk            },
   # { "name": "sll.d",      "func": rd_rj_rk            },
   # { "name": "srl.d",      "func": rd_rj_rk            },
   # { "name": "sra.d",      "func": rd_rj_rk            },
   # { "name": "rotr.w",     "func": rd_rj_rk            },
   # { "name": "rotr.d",     "func": rd_rj_rk            },
   # { "name": "slli.w",     "func": rd_rj_ui5           },
   # { "name": "slli.d",     "func": rd_rj_ui6           },
   # { "name": "srli.w",     "func": rd_rj_ui5           },
   # { "name": "srli.d",     "func": rd_rj_ui6           },
   # { "name": "srai.w",     "func": rd_rj_ui5           },
   # { "name": "srai.d",     "func": rd_rj_ui6           },
   # { "name": "rotri.w",    "func": rd_rj_ui5           },
   # { "name": "rotri.d",    "func": rd_rj_ui6           },
    { "name": "ext.w.h",    "func": rd_rj               },
   # { "name": "ext.w.b",    "func": rd_rj               },
   # { "name": "clo.w",      "func": rd_rj               },
   # { "name": "clz.w",      "func": rd_rj               },
   # { "name": "cto.w",      "func": rd_rj               },
   # { "name": "ctz.w",      "func": rd_rj               },
   # { "name": "clo.d",      "func": rd_rj               },
   # { "name": "clz.d",      "func": rd_rj               },
   # { "name": "cto.d",      "func": rd_rj               },
   # { "name": "ctz.d",      "func": rd_rj               },
   # { "name": "revb.2h",    "func": rd_rj               },
   # { "name": "revb.4h",    "func": rd_rj               },
   # { "name": "revb.2w",    "func": rd_rj               },
   # { "name": "revb.d",     "func": rd_rj               },
   # { "name": "revh.2w",    "func": rd_rj               },
   # { "name": "revh.d",     "func": rd_rj               },
   # { "name": "bitrev.4b",  "func": rd_rj               },
   # { "name": "bitrev.8b",  "func": rd_rj               },
   # { "name": "bitrev.w",   "func": rd_rj               },
   # { "name": "bitrev.d",   "func": rd_rj               },
   # { "name": "bytepick.w", "func": rd_rj_rk_sa2        },
   # { "name": "bytepick.d", "func": rd_rj_rk_sa3        },
   # { "name": "maskeqz",    "func": rd_rj_rk            },
   # { "name": "masknez",    "func": rd_rj_rk            },
   # { "name": "bstrins.w",  "func": rd_rj_msbw_lsbw     },
   # { "name": "bstrpick.w", "func": rd_rj_msbw_lsbw     },
   # { "name": "bstrins.d",  "func": rd_rj_msbd_lsbd     },
   # { "name": "bstrpick.d", "func": rd_rj_msbd_lsbd     },
]
n = 10
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
