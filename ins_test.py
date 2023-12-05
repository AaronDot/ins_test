import os
import numpy as np

def write(line, file):
    with open("dump.S", "r") as input:
        text = input.read()
        with open(file, "w") as output:
            output.write(text.replace("nop\n", line))

def build(line):
    write(line, "tmp.S")
    ret = os.system("gcc -nostdlib -static tmp.S show.c data.c -o tmp")
    if ret != 0:
        return ret
    ret = os.system("./tmp > want.txt 2>&1")
    if ret != 0:
        print("ret = ");
        return ret
    #return os.system("/usr/local/bin/valgrind --tool=none -q ./tmp > out.txt 2>&1")
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
                if lines1[i] != lines2[i]:
                    print("want: " + lines1[i] + "out: " + lines2[i])
                    return False
            return True


def test(name, func, n):
    for i in range(0, n):
        line = func(name, i)
        if build(line) != 0:
            print("Build failed!")
            return False
        if not diff():
            return False
    return True


def rand_imm(n, sign):
    min = 0 
    max = 1 << n
    if (sign):
        min = -(1 << (n - 1))
        max = 1 << (n - 1)
    imm = np.random.randint(min, max, 1, np.int32)
    return imm[0]

def vd_vj_vk(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, 0x0\n    "
    line += f"vld $vr2, $t0, 0x8\n    "
#    line += f"vld $vr1, $t0, 0xe8\n    "
#    line += f"vld $vr2, $t0, 0xf0\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_vk1(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"vld $vr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_rk(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"ld.d $r20, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $r20\n"
    return line

def vd_vj(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $vr1\n"
    return line

def vd_rj(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $r20\n"
    return line

def cd_vj(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"{name} $fcc0, $vr0\n"
    return line

def vd_si(name, n):
    line = f"{name} $vr0, -832\n"
    return line

def vd_vj_vk_va(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, 0x80\n    "
    line += f"vld $vr2, $t0, 0x70\n    "
    line += f"vld $vr3, $t0, 0xe0\n    "
#    line += f"vld $vr1, $t0, {0x8 * n}\n    "
#    line += f"vld $vr2, $t0, {0x8 * (n + 1)}\n    "
#    line += f"vld $vr3, $t0, {0x8 * (n + 1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2, $vr3\n"
    return line

def vd_rj_ui4(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui4 = rand_imm(4, False)
    line += f"{name} $vr0, $r20, {ui4}\n"
    return line

def vd_rj_ui3(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $vr0, $r20, {ui3}\n"
    return line

def vd_rj_ui2(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $vr0, $r20, {ui2}\n"
    return line

def vd_rj_ui1(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $vr0, $r20, {ui1}\n"
    return line

def vd_rj_si(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"{name} $vr0, $t0, {0x8 * n}\n"
    return line

def vd_rj_si_idx(name, n):
    line =  "la.local $t1, mem_j\n    "
    line =  "la.local $t0, out\n    "
    line += f"vld $vr1, $t1, {0x8 * n}\n    "
    line += f"{name} $vr1, $t0, 0, 1\n"
    return line

def rd_vj_ui4(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui4 = rand_imm(4, False)
    line += f"{name} $r20, $vr0, {ui4}\n"
    return line

def rd_vj_ui3(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $r20, $vr0, {ui3}\n"
    return line

def rd_vj_ui2(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $r20, $vr0, {ui2}\n"
    return line

def rd_vj_ui1(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $r20, $vr0, {ui1}\n"
    return line

def vd_vj_ui8(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui8 = rand_imm(8, False)
    line += f"{name} $vr0, $vr1, {ui8}\n"
    return line

def vd_vj_ui7(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui7 = rand_imm(7, False)
    line += f"{name} $vr0, $vr1, {ui7}\n"
    return line

def vd_vj_ui6(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui6 = rand_imm(6, False)
    line += f"{name} $vr0, $vr1, {ui6}\n"
    return line

def vd_vj_ui5(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui5 = rand_imm(5, False)
    line += f"{name} $vr0, $vr1, {ui5}\n"
    return line

def vd_vj_ui4(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, 0x0\n    "
    ui4 = rand_imm(4, False)
    print("ui4: %d" %ui4);
    #for i in range (0, 16, 1) :
    line += f"{name} $vr0, $vr1, 7\n"
    return line

def _vd_vj_ui4(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    #for i in range (0, 16, 1) :
    #ui4 = rand_imm(4, False)
    #    print("i: %d" %i);
    line += f"{name} $vr0, $vr1, 0\n"
    return line

def vd_vj_ui3(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $vr0, $vr1, {ui3}\n"
    return line

def vd_vj_ui2(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $vr0, $vr1, {ui2}\n"
    return line

def vd_vj_ui1(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $vr0, $vr1, {ui1}\n"
    return line

insts = [
   # { "name": "vsat.h",           "func": vd_vj_ui4 },

   # { "name": "vsrl.b",           "func": vd_vj_vk1 },
#    { "name": "vsrl.h",           "func": vd_vj_vk },
   # { "name": "vsrl.w",           "func": vd_vj_vk1 },
   # { "name": "vsrl.d",           "func": vd_vj_vk1 },
   # { "name": "vsra.b",           "func": vd_vj_vk1 },
   # { "name": "vsra.h",           "func": vd_vj_vk1 },
   # { "name": "vsra.w",           "func": vd_vj_vk1 },
   # { "name": "vsra.d",           "func": vd_vj_vk1 },
   # { "name": "vssrln.b.h",       "func": vd_vj_vk },
    { "name": "vssrln.h.w",       "func": vd_vj_vk1 },
   # { "name": "vssrln.w.d",       "func": vd_vj_vk1 },
   # { "name": "vssran.b.h",       "func": vd_vj_vk1 },
   # { "name": "vssran.h.w",       "func": vd_vj_vk1 },
   # { "name": "vssran.w.d",       "func": vd_vj_vk1 },
   # { "name": "vssrln.bu.h",      "func": vd_vj_vk1 },
   # { "name": "vssrln.hu.w",      "func": vd_vj_vk1 },
   # { "name": "vssrln.wu.d",      "func": vd_vj_vk1 },
]

n = 30
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
