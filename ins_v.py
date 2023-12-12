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

def vd_vj_vk_t(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, 0x0\n    "
    line += f"vld $vr2, $t0, 0x8\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_vk(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"vld $vr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_rk(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"ld.d $r20, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $r20\n"
    return line

def vd_vj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $vr1\n"
    return line

def vd_rj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $r20\n"
    return line

def cd_vj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0,  0x8\n    "
    line += f"{name} $fcc0, $vr0\n"
    return line

def vd_si13(name, n):
    line = f"{name} $vr0, -832\n"
    return line

def vd_vj_vk_va(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, 0x80\n    "
    line += f"vld $vr2, $t0, 0x70\n    "
    line += f"vld $vr3, $t0, 0xe0\n    "
#    line += f"vld $vr1, $t0, {0x8 * n}\n    "
#    line += f"vld $vr2, $t0, {0x8 * (n + 1)}\n    "
#    line += f"vld $vr3, $t0, {0x8 * (n + 1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2, $vr3\n"
    return line

def vd_rj_ui4(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui4 = rand_imm(4, False)
    line += f"{name} $vr0, $r20, {ui4}\n"
    return line

def vd_rj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $vr0, $r20, {ui3}\n"
    return line

def vd_rj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $vr0, $r20, {ui2}\n"
    return line

def vd_rj_ui1(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $vr0, $r20, {ui1}\n"
    return line

def vd_rj_si12(name, n):
    line =  "la.local $t0, mem_k\n    "
    si12 = rand_imm(12, True)
    line += f"{name} $vr0, $t0, {si12}\n"
    return line

def vd_rj_si12(name, n):
    line =  "la.local $t0, mem_k\n    "
    si12 = rand_imm(12, True)
    line += f"{name} $vr0, $t0, {0x8 * si12}\n"
    return line

def vd_rj_si11(name, n):
    line =  "la.local $t0, mem_k\n    "
    si11 = rand_imm(11, True)
    line += f"{name} $vr0, $t0, {0x8 * si11}\n"
    return line

def vd_rj_si10(name, n):
    line =  "la.local $t0, mem_k\n    "
    si10 = rand_imm(10, True)
    line += f"{name} $vr0, $t0, {si10}\n"
    return line

def vd_rj_si9(name, n):
    line =  "la.local $t0, mem_k\n    "
    si9 = rand_imm(9, True)
    line += f"{name} $vr0, $t0, {si9}\n"
    return line

def vd_rj_si8_idx(name, n):
    line =  "la.local $t1, mem_k\n    "
    line =  "la.local $t0, out\n    "
    line += f"vld $vr1, $t1, {0x8 * n}\n    "
    line += f"{name} $vr1, $t0, 0, 1\n"
    return line

def rd_vj_ui4(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui4 = rand_imm(4, False)
    line += f"{name} $r20, $vr0, {ui4}\n"
    return line

def rd_vj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $r20, $vr0, {ui3}\n"
    return line

def rd_vj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $r20, $vr0, {ui2}\n"
    return line

def rd_vj_ui1(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $r20, $vr0, {ui1}\n"
    return line

def vd_vj_ui8(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui8 = rand_imm(8, False)
    line += f"{name} $vr0, $vr1, {ui8}\n"
    return line

def vd_vj_ui7(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui7 = rand_imm(7, False)
    line += f"{name} $vr0, $vr1, {ui7}\n"
    return line

def vd_vj_ui6(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui6 = rand_imm(6, False)
    line += f"{name} $vr0, $vr1, {ui6}\n"
    return line

def vd_vj_ui5(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui5 = rand_imm(5, False)
    line += f"{name} $vr0, $vr1, {ui5}\n"
    return line

def vd_vj_si5(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    si5 = rand_imm(5, True)
    line += f"{name} $vr0, $vr1, {si5}\n"
    return line

def vd_vj_ui4(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui4 = rand_imm(4, False)
    line += f"{name} $vr0, $vr1, {ui4}\n"
    return line

def _vd_vj_ui4(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    #for i in range (0, 16, 1) :
    #ui4 = rand_imm(4, False)
    #    print("i: %d" %i);
    line += f"{name} $vr0, $vr1, 0\n"
    return line

def vd_vj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $vr0, $vr1, {ui3}\n"
    return line

def vd_vj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $vr0, $vr1, {ui2}\n"
    return line

def vd_vj_ui1(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $vr0, $vr1, {ui1}\n"
    return line

def vd_vj_vk_f(name, n):
    line =  "la.local $t0, datad\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"vld $vr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

insts = [



###########Vector integer arithmetic insns
   # { "name": "vadd.b",           "func": vd_vj_vk  },
   # { "name": "vadd.h",           "func": vd_vj_vk  },
   # { "name": "vadd.w",           "func": vd_vj_vk  },
   # { "name": "vadd.d",           "func": vd_vj_vk  },
   # { "name": "vadd.q",           "func": vd_vj_vk  },
   # { "name": "vsub.b",           "func": vd_vj_vk  },
   # { "name": "vsub.h",           "func": vd_vj_vk  },
   # { "name": "vsub.w",           "func": vd_vj_vk  },
   # { "name": "vsub.d",           "func": vd_vj_vk  },
   # { "name": "vsub.q",           "func": vd_vj_vk  },
   # { "name": "vaddi.bu",         "func": vd_vj_ui5 },
   # { "name": "vaddi.hu",         "func": vd_vj_ui5 },
   # { "name": "vaddi.wu",         "func": vd_vj_ui5 },
   # { "name": "vaddi.du",         "func": vd_vj_ui5 },
   # { "name": "vsubi.bu",         "func": vd_vj_ui5 },
   # { "name": "vsubi.hu",         "func": vd_vj_ui5 },
   # { "name": "vsubi.wu",         "func": vd_vj_ui5 },
   # { "name": "vsubi.du",         "func": vd_vj_ui5 },
   # { "name": "vneg.b",           "func": vd_vj     },
   # { "name": "vneg.h",           "func": vd_vj     },
   # { "name": "vneg.w",           "func": vd_vj     },
   # { "name": "vneg.d",           "func": vd_vj     },
   # { "name": "vsadd.b",          "func": vd_vj_vk  },
   # { "name": "vsadd.h",          "func": vd_vj_vk  },
   # { "name": "vsadd.w",          "func": vd_vj_vk  },
   # { "name": "vsadd.d",          "func": vd_vj_vk  },
   # { "name": "vsadd.bu",         "func": vd_vj_vk  },
   # { "name": "vsadd.hu",         "func": vd_vj_vk  },
   # { "name": "vsadd.wu",         "func": vd_vj_vk  },
   # { "name": "vsadd.du",         "func": vd_vj_vk  },
   # { "name": "vssub.b",          "func": vd_vj_vk  },
   # { "name": "vssub.h",          "func": vd_vj_vk  },
   # { "name": "vssub.w",          "func": vd_vj_vk  },
   # { "name": "vssub.d",          "func": vd_vj_vk  },
   # { "name": "vssub.bu",         "func": vd_vj_vk  },
   # { "name": "vssub.hu",         "func": vd_vj_vk  },
   # { "name": "vssub.wu",         "func": vd_vj_vk  },
   # { "name": "vssub.du",         "func": vd_vj_vk  },
   # { "name": "vhaddw.h.b",       "func": vd_vj_vk  },
   # { "name": "vhaddw.w.h",       "func": vd_vj_vk  },
   # { "name": "vhaddw.d.w",       "func": vd_vj_vk  },
   # { "name": "vhaddw.q.d",       "func": vd_vj_vk  },
   # { "name": "vhsubw.h.b",       "func": vd_vj_vk  },
   # { "name": "vhsubw.w.h",       "func": vd_vj_vk  },
   # { "name": "vhsubw.d.w",       "func": vd_vj_vk  },
   # { "name": "vhsubw.q.d",       "func": vd_vj_vk  },
   # { "name": "vhaddw.hu.bu",     "func": vd_vj_vk  },
   # { "name": "vhaddw.wu.hu",     "func": vd_vj_vk  },
   # { "name": "vhaddw.du.wu",     "func": vd_vj_vk  },
   # { "name": "vhaddw.qu.du",     "func": vd_vj_vk  },
   # { "name": "vhsubw.hu.bu",     "func": vd_vj_vk  },
   # { "name": "vhsubw.wu.hu",     "func": vd_vj_vk  },
   # { "name": "vhsubw.du.wu",     "func": vd_vj_vk  },
   # { "name": "vhsubw.qu.du",     "func": vd_vj_vk  },
   # { "name": "vaddwev.h.b",      "func": vd_vj_vk  },
   # { "name": "vaddwev.w.h",      "func": vd_vj_vk  },
   # { "name": "vaddwev.d.w",      "func": vd_vj_vk  },
   # { "name": "vaddwev.q.d",      "func": vd_vj_vk  },
   # { "name": "vsubwev.h.b",      "func": vd_vj_vk  },
   # { "name": "vsubwev.w.h",      "func": vd_vj_vk  },
   # { "name": "vsubwev.d.w",      "func": vd_vj_vk  },
   # { "name": "vsubwev.q.d",      "func": vd_vj_vk  },
   # { "name": "vaddwod.h.b",      "func": vd_vj_vk  },
   # { "name": "vaddwod.w.h",      "func": vd_vj_vk  },
   # { "name": "vaddwod.d.w",      "func": vd_vj_vk  },
   # { "name": "vaddwod.q.d",      "func": vd_vj_vk  },
   # { "name": "vsubwod.h.b",      "func": vd_vj_vk  },
   # { "name": "vsubwod.w.h",      "func": vd_vj_vk  },
   # { "name": "vsubwod.d.w",      "func": vd_vj_vk  },
   # { "name": "vsubwod.q.d",      "func": vd_vj_vk  },
   # { "name": "vaddwev.h.bu",     "func": vd_vj_vk  },
   # { "name": "vaddwev.w.hu",     "func": vd_vj_vk  },
   # { "name": "vaddwev.d.wu",     "func": vd_vj_vk  },
   # { "name": "vaddwev.q.du",     "func": vd_vj_vk  },
   # { "name": "vsubwev.h.bu",     "func": vd_vj_vk  },
   # { "name": "vsubwev.w.hu",     "func": vd_vj_vk  },
   # { "name": "vsubwev.d.wu",     "func": vd_vj_vk  },
   # { "name": "vsubwev.q.du",     "func": vd_vj_vk  },
   # { "name": "vaddwod.h.bu",     "func": vd_vj_vk  },
   # { "name": "vaddwod.w.hu",     "func": vd_vj_vk  },
   # { "name": "vaddwod.d.wu",     "func": vd_vj_vk  },
   # { "name": "vaddwod.q.du",     "func": vd_vj_vk  },
   # { "name": "vsubwod.h.bu",     "func": vd_vj_vk  },
   # { "name": "vsubwod.w.hu",     "func": vd_vj_vk  },
   # { "name": "vsubwod.d.wu",     "func": vd_vj_vk  },
   # { "name": "vsubwod.q.du",     "func": vd_vj_vk  },
   # { "name": "vaddwev.h.bu.b",   "func": vd_vj_vk  },
   # { "name": "vaddwev.w.hu.h",   "func": vd_vj_vk  },
   # { "name": "vaddwev.d.wu.w",   "func": vd_vj_vk  },
   # { "name": "vaddwev.q.du.d",   "func": vd_vj_vk  },
   # { "name": "vaddwod.h.bu.b",   "func": vd_vj_vk  },
   # { "name": "vaddwod.w.hu.h",   "func": vd_vj_vk  },
   # { "name": "vaddwod.d.wu.w",   "func": vd_vj_vk  },
   # { "name": "vaddwod.q.du.d",   "func": vd_vj_vk  },
   # { "name": "vavg.b",           "func": vd_vj_vk  },
   # { "name": "vavg.h",           "func": vd_vj_vk  },
   # { "name": "vavg.w",           "func": vd_vj_vk  },
   # { "name": "vavg.d",           "func": vd_vj_vk  },
   # { "name": "vavg.bu",          "func": vd_vj_vk  },
   # { "name": "vavg.hu",          "func": vd_vj_vk  },
   # { "name": "vavg.wu",          "func": vd_vj_vk  },
   # { "name": "vavg.du",          "func": vd_vj_vk  },
   # { "name": "vavgr.b",          "func": vd_vj_vk  },
   # { "name": "vavgr.h",          "func": vd_vj_vk  },
   # { "name": "vavgr.w",          "func": vd_vj_vk  },
   # { "name": "vavgr.d",          "func": vd_vj_vk  },
   # { "name": "vavgr.bu",         "func": vd_vj_vk  },
   # { "name": "vavgr.hu",         "func": vd_vj_vk  },
   # { "name": "vavgr.wu",         "func": vd_vj_vk  },
   # { "name": "vavgr.du",         "func": vd_vj_vk  },
   # { "name": "vabsd.b",          "func": vd_vj_vk  },
   # { "name": "vabsd.h",          "func": vd_vj_vk  },
   # { "name": "vabsd.w",          "func": vd_vj_vk  },
   # { "name": "vabsd.d",          "func": vd_vj_vk  },
   # { "name": "vabsd.bu",         "func": vd_vj_vk  },
   # { "name": "vabsd.hu",         "func": vd_vj_vk  },
   # { "name": "vabsd.wu",         "func": vd_vj_vk  },
   # { "name": "vabsd.du",         "func": vd_vj_vk  },
   # { "name": "vadda.b",          "func": vd_vj_vk  },
   # { "name": "vadda.h",          "func": vd_vj_vk  },
   # { "name": "vadda.w",          "func": vd_vj_vk  },
   # { "name": "vadda.d",          "func": vd_vj_vk  },
   # { "name": "vmax.b",           "func": vd_vj_vk  },
   # { "name": "vmax.h",           "func": vd_vj_vk  },
   # { "name": "vmax.w",           "func": vd_vj_vk  },
   # { "name": "vmax.d",           "func": vd_vj_vk  },
   # { "name": "vmax.bu",          "func": vd_vj_vk  },
   # { "name": "vmax.hu",          "func": vd_vj_vk  },
   # { "name": "vmax.wu",          "func": vd_vj_vk  },
   # { "name": "vmax.du",          "func": vd_vj_vk  },
   # { "name": "vmin.b",           "func": vd_vj_vk  },
   # { "name": "vmin.h",           "func": vd_vj_vk  },
   # { "name": "vmin.w",           "func": vd_vj_vk  },
   # { "name": "vmin.d",           "func": vd_vj_vk  },
   # { "name": "vmin.bu",          "func": vd_vj_vk  },
   # { "name": "vmin.hu",          "func": vd_vj_vk  },
   # { "name": "vmin.wu",          "func": vd_vj_vk  },
   # { "name": "vmin.du",          "func": vd_vj_vk  },
   # { "name": "vmaxi.b",          "func": vd_vj_si5 },
   # { "name": "vmaxi.h",          "func": vd_vj_si5 },
   # { "name": "vmaxi.w",          "func": vd_vj_si5 },
   # { "name": "vmaxi.d",          "func": vd_vj_si5 },
   # { "name": "vmini.b",          "func": vd_vj_si5 },
   # { "name": "vmini.h",          "func": vd_vj_si5 },
   # { "name": "vmini.w",          "func": vd_vj_si5 },
   # { "name": "vmini.d",          "func": vd_vj_si5 },
   # { "name": "vmaxi.bu",         "func": vd_vj_ui5 },
   # { "name": "vmaxi.hu",         "func": vd_vj_ui5 },
   # { "name": "vmaxi.wu",         "func": vd_vj_ui5 },
   # { "name": "vmaxi.du",         "func": vd_vj_ui5 },
   # { "name": "vmini.bu",         "func": vd_vj_ui5 },
   # { "name": "vmini.hu",         "func": vd_vj_ui5 },
   # { "name": "vmini.wu",         "func": vd_vj_ui5 },
   # { "name": "vmini.du",         "func": vd_vj_ui5 },
   # { "name": "vmul.b",           "func": vd_vj_vk  },
   # { "name": "vmul.h",           "func": vd_vj_vk  },
   # { "name": "vmul.w",           "func": vd_vj_vk  },
   # { "name": "vmul.d",           "func": vd_vj_vk  },
   # { "name": "vmuh.b",           "func": vd_vj_vk  },
   # { "name": "vmuh.h",           "func": vd_vj_vk  },
   # { "name": "vmuh.w",           "func": vd_vj_vk  },
   # { "name": "vmuh.d",           "func": vd_vj_vk  },
   # { "name": "vmuh.bu",          "func": vd_vj_vk  },
   # { "name": "vmuh.hu",          "func": vd_vj_vk  },
   # { "name": "vmuh.wu",          "func": vd_vj_vk  },
   # { "name": "vmuh.du",          "func": vd_vj_vk  },
   # { "name": "vmulwev.h.b",      "func": vd_vj_vk  },
   # { "name": "vmulwev.w.h",      "func": vd_vj_vk  },
   # { "name": "vmulwev.d.w",      "func": vd_vj_vk  },
   # { "name": "vmulwev.q.d",      "func": vd_vj_vk  },
   # { "name": "vmulwod.h.b",      "func": vd_vj_vk  },
   # { "name": "vmulwod.w.h",      "func": vd_vj_vk  },
   # { "name": "vmulwod.d.w",      "func": vd_vj_vk  },
   # { "name": "vmulwod.q.d",      "func": vd_vj_vk  },
   # { "name": "vmulwev.h.bu",     "func": vd_vj_vk  },
   # { "name": "vmulwev.w.hu",     "func": vd_vj_vk  },
   # { "name": "vmulwev.d.wu",     "func": vd_vj_vk  },
   # { "name": "vmulwev.q.du",     "func": vd_vj_vk  },
   # { "name": "vmulwod.h.bu",     "func": vd_vj_vk  },
   # { "name": "vmulwod.w.hu",     "func": vd_vj_vk  },
   # { "name": "vmulwod.d.wu",     "func": vd_vj_vk  },
   # { "name": "vmulwod.q.du",     "func": vd_vj_vk  },
   # { "name": "vmulwev.h.bu.b",   "func": vd_vj_vk  },
   # { "name": "vmulwev.w.hu.h",   "func": vd_vj_vk  },
   # { "name": "vmulwev.d.wu.w",   "func": vd_vj_vk  },
   # { "name": "vmulwev.q.du.d",   "func": vd_vj_vk  }, #TODO
   # { "name": "vmulwod.h.bu.b",   "func": vd_vj_vk  },
   # { "name": "vmulwod.w.hu.h",   "func": vd_vj_vk  },
   # { "name": "vmulwod.d.wu.w",   "func": vd_vj_vk  },
   # { "name": "vmulwod.q.du.d",   "func": vd_vj_vk  }, #TODO
   # { "name": "vmadd.b",          "func": vd_vj_vk  },
   # { "name": "vmadd.h",          "func": vd_vj_vk  },
   # { "name": "vmadd.w",          "func": vd_vj_vk  },
   # { "name": "vmadd.d",          "func": vd_vj_vk  },
   # { "name": "vmsub.b",          "func": vd_vj_vk  },
   # { "name": "vmsub.h",          "func": vd_vj_vk  },
   # { "name": "vmsub.w",          "func": vd_vj_vk  },
   # { "name": "vmsub.d",          "func": vd_vj_vk  },
   # { "name": "vmaddwev.h.b",     "func": vd_vj_vk  },
   # { "name": "vmaddwev.w.h",     "func": vd_vj_vk  },
   # { "name": "vmaddwev.d.w",     "func": vd_vj_vk  },
   # { "name": "vmaddwev.q.d",     "func": vd_vj_vk  },
   # { "name": "vmaddwod.h.b",     "func": vd_vj_vk  },
   # { "name": "vmaddwod.w.h",     "func": vd_vj_vk  },
   # { "name": "vmaddwod.d.w",     "func": vd_vj_vk  },
   # { "name": "vmaddwod.q.d",     "func": vd_vj_vk  },
   # { "name": "vmaddwev.h.bu",    "func": vd_vj_vk  },
   # { "name": "vmaddwev.w.hu",    "func": vd_vj_vk  },
   # { "name": "vmaddwev.d.wu",    "func": vd_vj_vk  },
   # { "name": "vmaddwev.q.du",    "func": vd_vj_vk  },
   # { "name": "vmaddwod.h.bu",    "func": vd_vj_vk  },
   # { "name": "vmaddwod.w.hu",    "func": vd_vj_vk  },
   # { "name": "vmaddwod.d.wu",    "func": vd_vj_vk  },
   # { "name": "vmaddwod.q.du",    "func": vd_vj_vk  },
   # { "name": "vmaddwev.h.bu.b",  "func": vd_vj_vk  },
   # { "name": "vmaddwev.w.hu.h",  "func": vd_vj_vk  },
   # { "name": "vmaddwev.d.wu.w",  "func": vd_vj_vk  },
   # { "name": "vmaddwev.q.du.d",  "func": vd_vj_vk  }, #TODO
   # { "name": "vmaddwod.h.bu.b",  "func": vd_vj_vk  },
   # { "name": "vmaddwod.w.hu.h",  "func": vd_vj_vk  },
   # { "name": "vmaddwod.d.wu.w",  "func": vd_vj_vk  },
   # { "name": "vmaddwod.q.du.d",  "func": vd_vj_vk  }, #TODO
   # { "name": "vdiv.b",           "func": vd_vj_vk  },
   # { "name": "vdiv.h",           "func": vd_vj_vk  },
   # { "name": "vdiv.w",           "func": vd_vj_vk  },
   # { "name": "vdiv.d",           "func": vd_vj_vk  },
   # { "name": "vdiv.bu",          "func": vd_vj_vk  },
   # { "name": "vdiv.hu",          "func": vd_vj_vk  },
   # { "name": "vdiv.wu",          "func": vd_vj_vk  },
   # { "name": "vdiv.du",          "func": vd_vj_vk  },
   # { "name": "vmod.b",           "func": vd_vj_vk  },
   # { "name": "vmod.h",           "func": vd_vj_vk  },
   # { "name": "vmod.w",           "func": vd_vj_vk  },
   # { "name": "vmod.d",           "func": vd_vj_vk  },
   # { "name": "vmod.bu",          "func": vd_vj_vk  },
   # { "name": "vmod.hu",          "func": vd_vj_vk  },
   # { "name": "vmod.wu",          "func": vd_vj_vk  },
   # { "name": "vmod.du",          "func": vd_vj_vk  },
   # { "name": "vsat.b",           "func": vd_vj_ui3 },
   # { "name": "vsat.h",           "func": vd_vj_ui4 },
   # { "name": "vsat.w",           "func": vd_vj_ui5 },
   # { "name": "vsat.d",           "func": vd_vj_ui6 },
   # { "name": "vsat.bu",          "func": vd_vj_ui3 },
   # { "name": "vsat.hu",          "func": vd_vj_ui4 },
   # { "name": "vsat.wu",          "func": vd_vj_ui5 },
   # { "name": "vsat.du",          "func": vd_vj_ui6 },
   # { "name": "vexth.h.b",        "func": vd_vj     },
   # { "name": "vexth.w.h",        "func": vd_vj     },
   # { "name": "vexth.d.w",        "func": vd_vj     },
   # { "name": "vexth.q.d",        "func": vd_vj     },
   # { "name": "vexth.hu.bu",      "func": vd_vj     },
   # { "name": "vexth.wu.hu",      "func": vd_vj     },
   # { "name": "vexth.du.wu",      "func": vd_vj     },
   # { "name": "vexth.qu.du",      "func": vd_vj     },
   # { "name": "vsigncov.b",       "func": vd_vj_vk  },
   # { "name": "vsigncov.h",       "func": vd_vj_vk  },
   # { "name": "vsigncov.w",       "func": vd_vj_vk  },
   # { "name": "vsigncov.d",       "func": vd_vj_vk  },
   # { "name": "vmskltz.b",        "func": vd_vj     },
   # { "name": "vmskltz.h",        "func": vd_vj     },
   # { "name": "vmskltz.w",        "func": vd_vj     },
   # { "name": "vmskltz.d",        "func": vd_vj     },
   # { "name": "vmskgez.b",        "func": vd_vj     },
   # { "name": "vmsknz.b",         "func": vd_vj     },
   # { "name": "vldi",             "func": vd_si13   },

##############Vector bit operation insns
   # { "name": "vand.v",           "func": vd_vj_vk  },
   # { "name": "vor.v",            "func": vd_vj_vk  },
   # { "name": "vxor.v",           "func": vd_vj_vk  },
   # { "name": "vnor.v",           "func": vd_vj_vk  },
   # { "name": "vandn.v",          "func": vd_vj_vk  },
   # { "name": "vorn.v",           "func": vd_vj_vk  },
   # { "name": "vandi.b",          "func": vd_vj_ui8 },
   # { "name": "vori.b",           "func": vd_vj_ui8 },
   # { "name": "vxori.b",          "func": vd_vj_ui8 },
   # { "name": "vnori.b",          "func": vd_vj_ui8 },
   # { "name": "vsll.b",           "func": vd_vj_vk  },
   # { "name": "vsll.h",           "func": vd_vj_vk  },
   # { "name": "vsll.w",           "func": vd_vj_vk  },
   # { "name": "vsll.d",           "func": vd_vj_vk  },
   # { "name": "vsrl.b",           "func": vd_vj_vk  },
   # { "name": "vsrl.h",           "func": vd_vj_vk  },
   # { "name": "vsrl.w",           "func": vd_vj_vk  },
   # { "name": "vsrl.d",           "func": vd_vj_vk  },
   # { "name": "vsra.b",           "func": vd_vj_vk  },
   # { "name": "vsra.h",           "func": vd_vj_vk  },
   # { "name": "vsra.w",           "func": vd_vj_vk  },
   # { "name": "vsra.d",           "func": vd_vj_vk  },
   # { "name": "vrotr.b",          "func": vd_vj_vk  },
   # { "name": "vrotr.h",          "func": vd_vj_vk  },
   # { "name": "vrotr.w",          "func": vd_vj_vk  },
   # { "name": "vrotr.d",          "func": vd_vj_vk  },
   # { "name": "vslli.b",          "func": vd_vj_ui3 },
   # { "name": "vslli.h",          "func": vd_vj_ui4 },
   # { "name": "vslli.w",          "func": vd_vj_ui5 },
   # { "name": "vslli.d",          "func": vd_vj_ui6 },
   # { "name": "vsrli.b",          "func": vd_vj_ui3 },
   # { "name": "vsrli.h",          "func": vd_vj_ui4 },
   # { "name": "vsrli.w",          "func": vd_vj_ui5 },
   # { "name": "vsrli.d",          "func": vd_vj_ui6 },
   # { "name": "vsrai.b",          "func": vd_vj_ui3 },
   # { "name": "vsrai.h",          "func": vd_vj_ui4 },
   # { "name": "vsrai.w",          "func": vd_vj_ui5 },
   # { "name": "vsrai.d",          "func": vd_vj_ui6 },
   # { "name": "vrotri.b",         "func": vd_vj_ui3 },
   # { "name": "vrotri.h",         "func": vd_vj_ui4 },
   # { "name": "vrotri.w",         "func": vd_vj_ui5 },
   # { "name": "vrotri.d",         "func": vd_vj_ui6 },
   # { "name": "vsllwil.h.b",      "func": vd_vj_ui3 },
   # { "name": "vsllwil.w.h",      "func": vd_vj_ui4 },
   # { "name": "vsllwil.d.w",      "func": vd_vj_ui5 },
   # { "name": "vextl.q.d",        "func": vd_vj     },
   # { "name": "vsllwil.hu.bu",    "func": vd_vj_ui3 },
   # { "name": "vsllwil.wu.hu",    "func": vd_vj_ui4 },
   # { "name": "vsllwil.du.wu",    "func": vd_vj_ui5 },
   # { "name": "vextl.qu.du",      "func": vd_vj     },
   # { "name": "vsrlr.b",          "func": vd_vj_vk  },
   # { "name": "vsrlr.h",          "func": vd_vj_vk  },
   # { "name": "vsrlr.w",          "func": vd_vj_vk  },
   # { "name": "vsrlr.d",          "func": vd_vj_vk  },
   # { "name": "vsrar.b",          "func": vd_vj_vk  },
   # { "name": "vsrar.h",          "func": vd_vj_vk  },
   # { "name": "vsrar.w",          "func": vd_vj_vk  },
   # { "name": "vsrar.d",          "func": vd_vj_vk  },
   # { "name": "vsrlri.b",         "func": vd_vj_ui3 },
   # { "name": "vsrlri.h",         "func": vd_vj_ui4 },
   # { "name": "vsrlri.w",         "func": vd_vj_ui5 },
   # { "name": "vsrlri.d",         "func": vd_vj_ui6 },
   # { "name": "vsrari.b",         "func": vd_vj_ui3 },
   # { "name": "vsrari.h",         "func": vd_vj_ui4 },
   # { "name": "vsrari.w",         "func": vd_vj_ui5 },
   # { "name": "vsrari.d",         "func": vd_vj_ui6 },
   # { "name": "vsrln.b.h",        "func": vd_vj_vk  },
   # { "name": "vsrln.h.w",        "func": vd_vj_vk  },
   # { "name": "vsrln.w.d",        "func": vd_vj_vk  },
   # { "name": "vsran.b.h",        "func": vd_vj_vk  },
   # { "name": "vsran.h.w",        "func": vd_vj_vk  },
   # { "name": "vsran.w.d",        "func": vd_vj_vk  },
   # { "name": "vsrlni.b.h",       "func": vd_vj_ui4 },
   # { "name": "vsrlni.h.w",       "func": vd_vj_ui5 },
   # { "name": "vsrlni.w.d",       "func": vd_vj_ui6 },

   # { "name": "vsrlni.d.q",       "func": vd_vj_ui7 }, # TODO
   # { "name": "vsrlrn.b.h",       "func": vd_vj_vk },
   # { "name": "vsrlrn.h.w",       "func": vd_vj_vk },
   # { "name": "vsrlrn.w.d",       "func": vd_vj_vk },
   # { "name": "vsrarn.b.h",       "func": vd_vj_vk },
   # { "name": "vsrarn.h.w",       "func": vd_vj_vk },
   # { "name": "vsrarn.w.d",       "func": vd_vj_vk },
   # { "name": "vssrln.b.h",       "func": vd_vj_vk },
   # { "name": "vssrln.h.w",       "func": vd_vj_vk },
   # { "name": "vssrln.w.d",       "func": vd_vj_vk },
   # { "name": "vssran.b.h",       "func": vd_vj_vk },
   # { "name": "vssran.h.w",       "func": vd_vj_vk },
   # { "name": "vssran.w.d",       "func": vd_vj_vk },
   # { "name": "vssrln.bu.h",      "func": vd_vj_vk },
   # { "name": "vssrln.hu.w",      "func": vd_vj_vk },
   # { "name": "vssrln.wu.d",      "func": vd_vj_vk },
   # { "name": "vssran.bu.h",      "func": vd_vj_vk }, #bad
   # { "name": "vssran.hu.w",      "func": vd_vj_vk }, #bad
   # { "name": "vssran.wu.d",      "func": vd_vj_vk }, #bad
   # { "name": "vssrlrn.b.h",      "func": vd_vj_vk },
   # { "name": "vssrlrn.h.w",      "func": vd_vj_vk },
   # { "name": "vssrlrn.w.d",      "func": vd_vj_vk },
   # { "name": "vssrarn.b.h",      "func": vd_vj_vk },
   # { "name": "vssrarn.h.w",      "func": vd_vj_vk },
   # { "name": "vssrarn.w.d",      "func": vd_vj_vk },
   # { "name": "vssrlrn.bu.h",      "func": vd_vj_vk },
   # { "name": "vssrlrn.hu.w",      "func": vd_vj_vk },
   # { "name": "vssrlrn.wu.d",      "func": vd_vj_vk },
   # { "name": "vssran.bu.h",      "func": vd_vj_vk }, #bad
   # { "name": "vssran.hu.w",      "func": vd_vj_vk }, #bad
   # { "name": "vssran.wu.d",      "func": vd_vj_vk }, #bad
   # { "name": "vsrani.b.h",       "func": vd_vj_ui4 },
   # { "name": "vsrani.h.w",       "func": vd_vj_ui5 },
   # { "name": "vsrani.w.d",       "func": vd_vj_ui6 },
   # { "name": "vsrani.d.q",       "func": vd_vj_ui7 }, # TODO
   # { "name": "vsrlrni.b.h",      "func": vd_vj_ui4 },
   # { "name": "vsrlrni.h.w",      "func": vd_vj_ui5 },
   # { "name": "vsrlrni.w.d",      "func": vd_vj_ui6 },
   # { "name": "vsrlrni.d.q",      "func": vd_vj_ui7 }, # TODO
   # { "name": "vsrarni.b.h",      "func": vd_vj_ui4 },
   # { "name": "vsrarni.h.w",      "func": vd_vj_ui5 },
   # { "name": "vsrarni.w.d",      "func": vd_vj_ui6 },
   # { "name": "vsrarni.d.q",      "func": vd_vj_ui7 }, # TODO
   # { "name": "vssrlni.b.h",      "func":  _vd_vj_ui4 },
   # { "name": "vssrlni.h.w",      "func": vd_vj_ui5 },
   # { "name": "vssrlni.w.d",      "func": vd_vj_ui6 },
   # { "name": "vssrlni.d.q",      "func": vd_vj_ui7 }, # TODO

   # { "name": "vclo.b",              "func": vd_vj },
   # { "name": "vclo.h",              "func": vd_vj },
   # { "name": "vclo.w",              "func": vd_vj },
   # { "name": "vclo.d",              "func": vd_vj },
   # { "name": "vclz.b",              "func": vd_vj },
   # { "name": "vclz.h",              "func": vd_vj },
   # { "name": "vclz.w",              "func": vd_vj },
   # { "name": "vclz.d",              "func": vd_vj },
   # { "name": "vpcnt.b",             "func": vd_vj },
   # { "name": "vpcnt.h",             "func": vd_vj },
   # { "name": "vpcnt.w",             "func": vd_vj },
   # { "name": "vpcnt.d",             "func": vd_vj },
   # { "name": "vbitclr.b",           "func": vd_vj_vk },
   # { "name": "vbitclr.h",           "func": vd_vj_vk },
   # { "name": "vbitclr.w",           "func": vd_vj_vk },
   # { "name": "vbitclr.d",           "func": vd_vj_vk },
   # { "name": "vbitset.b",           "func": vd_vj_vk },
   # { "name": "vbitset.h",           "func": vd_vj_vk },
   # { "name": "vbitset.w",           "func": vd_vj_vk },
   # { "name": "vbitset.d",           "func": vd_vj_vk },
   # { "name": "vbitrev.b",           "func": vd_vj_vk },
   # { "name": "vbitrev.h",           "func": vd_vj_vk },
   # { "name": "vbitrev.w",           "func": vd_vj_vk },
   # { "name": "vbitrev.d",           "func": vd_vj_vk },
   # { "name": "vbitclri.b",          "func": vd_vj_ui3 },
   # { "name": "vbitclri.h",          "func": vd_vj_ui4 },
   # { "name": "vbitclri.w",          "func": vd_vj_ui5 },
   # { "name": "vbitclri.d",          "func": vd_vj_ui6 },
   # { "name": "vbitseti.b",          "func": vd_vj_ui3 },
   # { "name": "vbitseti.h",          "func": vd_vj_ui4 },
   # { "name": "vbitseti.w",          "func": vd_vj_ui5 },
   # { "name": "vbitseti.d",          "func": vd_vj_ui6 },
   # { "name": "vbitrevi.b",          "func": vd_vj_ui3 },
   # { "name": "vbitrevi.h",          "func": vd_vj_ui4 },
   # { "name": "vbitrevi.w",          "func": vd_vj_ui5 },
   # { "name": "vbitrevi.d",          "func": vd_vj_ui6 },

###########Vector Floating-point Operation insns
   # { "name": "vfadd.s",           "func": vd_vj_vk_f },


################Vector comparison and selection insns 
   # { "name": "vseq.b",           "func": vd_vj_vk    },
   # { "name": "vseq.h",           "func": vd_vj_vk    },
   # { "name": "vseq.w",           "func": vd_vj_vk    },
   # { "name": "vseq.d",           "func": vd_vj_vk    },
   # { "name": "vseqi.b",          "func": vd_vj_si5   },
   # { "name": "vseqi.h",          "func": vd_vj_si5   },
   # { "name": "vseqi.w",          "func": vd_vj_si5   },
   # { "name": "vseqi.d",          "func": vd_vj_si5   },
   # { "name": "vsle.b",           "func": vd_vj_vk    },
   # { "name": "vsle.h",           "func": vd_vj_vk    },
   # { "name": "vsle.w",           "func": vd_vj_vk    },
   # { "name": "vsle.d",           "func": vd_vj_vk    },
   # { "name": "vslei.b",          "func": vd_vj_si5   },
   # { "name": "vslei.h",          "func": vd_vj_si5   },
   # { "name": "vslei.w",          "func": vd_vj_si5   },
   # { "name": "vslei.d",          "func": vd_vj_si5   },
   # { "name": "vsle.bu",          "func": vd_vj_vk    },
   # { "name": "vsle.hu",          "func": vd_vj_vk    },
   # { "name": "vsle.wu",          "func": vd_vj_vk    },
   # { "name": "vsle.du",          "func": vd_vj_vk    },
   # { "name": "vslei.bu",         "func": vd_vj_ui5   },
   # { "name": "vslei.hu",         "func": vd_vj_ui5   },
   # { "name": "vslei.wu",         "func": vd_vj_ui5   },
   # { "name": "vslei.du",         "func": vd_vj_ui5   },
   # { "name": "vslt.b",           "func": vd_vj_vk    },
   # { "name": "vslt.h",           "func": vd_vj_vk    },
   # { "name": "vslt.w",           "func": vd_vj_vk    },
   # { "name": "vslt.d",           "func": vd_vj_vk    },
   # { "name": "vslti.b",          "func": vd_vj_si5   },
   # { "name": "vslti.h",          "func": vd_vj_si5   },
   # { "name": "vslti.w",          "func": vd_vj_si5   },
   # { "name": "vslti.d",          "func": vd_vj_si5   },
   # { "name": "vslt.bu",          "func": vd_vj_vk    },
   # { "name": "vslt.hu",          "func": vd_vj_vk    },
   # { "name": "vslt.wu",          "func": vd_vj_vk    },
   # { "name": "vslt.du",          "func": vd_vj_vk    },
   # { "name": "vslti.bu",         "func": vd_vj_ui5   },
   # { "name": "vslti.hu",         "func": vd_vj_ui5   },
   # { "name": "vslti.wu",         "func": vd_vj_ui5   },
   # { "name": "vslti.du",         "func": vd_vj_ui5   },
   # { "name": "vbitsel.v",        "func": vd_vj_vk_va },
   # { "name": "vbitseli.b",       "func": vd_vj_ui8   },
   # { "name": "vseteqz.v",        "func": cd_vj       },
   # { "name": "vsetnez.v",        "func": cd_vj       },
   # { "name": "vsetanyeqz.b",     "func": cd_vj       },
   # { "name": "vsetanyeqz.h",     "func": cd_vj       },
   # { "name": "vsetanyeqz.w",     "func": cd_vj       },
   # { "name": "vsetanyeqz.d",     "func": cd_vj       },
   # { "name": "vsetallnez.b",     "func": cd_vj       },
   # { "name": "vsetallnez.h",     "func": cd_vj       },
   # { "name": "vsetallnez.w",     "func": cd_vj       },
   # { "name": "vsetallnez.d",     "func": cd_vj       },

###########Vector moving and shuffling insns
   # { "name": "vinsgr2vr.b",      "func": vd_rj_ui4   },
   # { "name": "vinsgr2vr.h",      "func": vd_rj_ui3   },
   # { "name": "vinsgr2vr.w",      "func": vd_rj_ui2   },
   # { "name": "vinsgr2vr.d",      "func": vd_rj_ui1   },
   # { "name": "vpickve2gr.b",     "func": rd_vj_ui4   },
   # { "name": "vpickve2gr.h",     "func": rd_vj_ui3   },
   # { "name": "vpickve2gr.w",     "func": rd_vj_ui2   },
   # { "name": "vpickve2gr.d",     "func": rd_vj_ui1   },
   # { "name": "vpickve2gr.bu",    "func": rd_vj_ui4   },
   # { "name": "vpickve2gr.hu",    "func": rd_vj_ui3   },
   # { "name": "vpickve2gr.wu",    "func": rd_vj_ui2   },
   # { "name": "vpickve2gr.du",    "func": rd_vj_ui1   },
   # { "name": "vreplgr2vr.b",     "func": vd_rj       },
   # { "name": "vreplgr2vr.h",     "func": vd_rj       },
   # { "name": "vreplgr2vr.w",     "func": vd_rj       },
   # { "name": "vreplgr2vr.d",     "func": vd_rj       },
   # { "name": "vreplve.b",        "func": vd_vj_rk    },
   # { "name": "vreplve.h",        "func": vd_vj_rk    },
   # { "name": "vreplve.w",        "func": vd_vj_rk    },
   # { "name": "vreplve.d",        "func": vd_vj_rk    },
   # { "name": "vreplvei.b",       "func": vd_vj_ui4   },
   # { "name": "vreplvei.h",       "func": vd_vj_ui3   },
   # { "name": "vreplvei.w",       "func": vd_vj_ui2   },
   # { "name": "vreplvei.d",       "func": vd_vj_ui1   },
   # { "name": "vbsll.v",          "func": vd_vj_ui5   },
   # { "name": "vbsrl.v",          "func": vd_vj_ui5   },
   # { "name": "vpackev.b",        "func": vd_vj_vk    },
   # { "name": "vpackev.h",        "func": vd_vj_vk    },
   # { "name": "vpackev.w",        "func": vd_vj_vk    },
   # { "name": "vpackev.d",        "func": vd_vj_vk    },
   # { "name": "vpackod.b",        "func": vd_vj_vk    },
   # { "name": "vpackod.h",        "func": vd_vj_vk    },
   # { "name": "vpackod.w",        "func": vd_vj_vk    },
   # { "name": "vpackod.d",        "func": vd_vj_vk    },
   # { "name": "vpickev.b",        "func": vd_vj_vk    },
   # { "name": "vpickev.h",        "func": vd_vj_vk    },
   # { "name": "vpickev.w",        "func": vd_vj_vk    },
   # { "name": "vpickev.d",        "func": vd_vj_vk    },
   # { "name": "vpickod.b",        "func": vd_vj_vk    },
   # { "name": "vpickod.h",        "func": vd_vj_vk    },
   # { "name": "vpickod.w",        "func": vd_vj_vk    },
   # { "name": "vpickod.d",        "func": vd_vj_vk    },
   # { "name": "vilvh.b",          "func": vd_vj_vk    },
   # { "name": "vilvh.h",          "func": vd_vj_vk    },
   # { "name": "vilvh.w",          "func": vd_vj_vk    },
   # { "name": "vilvh.d",          "func": vd_vj_vk    },
   # { "name": "vilvl.b",          "func": vd_vj_vk    },
   # { "name": "vilvl.h",          "func": vd_vj_vk    },
   # { "name": "vilvl.w",          "func": vd_vj_vk    },
   # { "name": "vilvl.d",          "func": vd_vj_vk    },
   # { "name": "vshuf.b",          "func": vd_vj_vk_va },
   # { "name": "vshuf.h",          "func": vd_vj_vk    },
   # { "name": "vshuf.w",          "func": vd_vj_vk    },
   # { "name": "vshuf.d",          "func": vd_vj_vk    },
   # { "name": "vshuf4i.b",        "func": vd_vj_ui8   },
   # { "name": "vshuf4i.h",        "func": vd_vj_ui8   },
   # { "name": "vshuf4i.w",        "func": vd_vj_ui8   },
   # { "name": "vshuf4i.d",        "func": vd_vj_ui8   },
   # { "name": "vpermi.w",         "func": vd_vj_ui8   },
   # { "name": "vextrins.b",       "func": vd_vj_ui8   },
   # { "name": "vextrins.h",       "func": vd_vj_ui8   },
   # { "name": "vextrins.w",       "func": vd_vj_ui8   },
   # { "name": "vextrins.d",       "func": vd_vj_ui8   },

###########Vector load/store insns
   # { "name": "vld",              "func": vd_vj_si12    },
   # { "name": "vst",              "func": vd_vj_si12    },
   # { "name": "vldx",             "func": vd_vj_rk      },
   # { "name": "vstx",             "func": vd_vj_rk      },
   # { "name": "vldrepl.b",        "func": vd_rj_si12    },
   # { "name": "vldrepl.h",        "func": vd_rj_si11    },
   # { "name": "vldrepl.w",        "func": vd_rj_si10    },
   # { "name": "vldrepl.d",        "func": vd_rj_si9     },
   # { "name": "vstelm.b",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.h",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.w",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.d",         "func": vd_rj_si8_idx },
]

n = 30
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
