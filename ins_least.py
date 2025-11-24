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
    return os.system("../out/bin/valgrind --tool=none -q ./tmp > out.txt 2>&1")


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
    line +=  "la.local $t1, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * 2}\n    "
    line += f"vld $vr2, $t1, {0x8 * 0}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_vk(name, n):
    line =  "la.local $t0, mem_k\n    "
    #line += f"vld $vr0, $t0, 0x40\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"vld $vr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def xd_xj_xk(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, 0x40\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    line += f"xvld $xr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $xr0, $xr1, $xr2\n"
    return line

def vd_vj_rk(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"ld.d $r20, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $r20\n"
    return line

def xd_xj_rk(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    line += f"ld.d $r20, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $xr0, $xr1, $r20\n"
    return line

def vd_vj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $vr1\n"
    return line

def xd_xj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    line += f"{name} $xr0, $xr1\n"
    return line

def vd_rj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $r20\n"
    return line

def xd_rj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    line += f"{name} $xr0, $r20\n"
    return line

def cd_vj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"{name} $fcc1, $vr0\n"
    return line

def cd_xj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    line += f"{name} $fcc1, $xr0\n"
    return line

def vd_si13(name, n):
    si13 = rand_imm(13, True)
    print("si13: %d" %si13);
    line = f"{name} $vr0, {si13}\n"
    #line = f"{name} $vr0, -1490\n"
    #line = f"{name} $vr0, -66\n"
    #line = f"{name} $vr0, -832\n"
    return line

def xd_si13(name, n):
    si13 = rand_imm(13, True)
    print("si13: %d" %si13);
    line = f"{name} $xr0, {si13}\n"
    #line = f"{name} $xr0, -1490\n"
    #line = f"{name} $xr0, -66\n"
    #line = f"{name} $xr0, -832\n"
    return line

def vd_vj_vk_va(name, n):
    line =  "la.local $t0, mem_k\n    "
#    line += f"vld $vr1, $t0, 0x80\n    "
#    line += f"vld $vr2, $t0, 0x70\n    "
#    line += f"vld $vr3, $t0, 0xe0\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"vld $vr2, $t0, {0x8 * (n + 1)}\n    "
    line += f"vld $vr3, $t0, {0x8 * (n + 1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2, $vr3\n"
    return line

def xd_xj_xk_xa(name, n):
    line =  "la.local $t0, mem_k\n    "
#    line += f"vld $vr1, $t0, 0x80\n    "
#    line += f"vld $vr2, $t0, 0x70\n    "
#    line += f"vld $vr3, $t0, 0xe0\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    line += f"xvld $xr2, $t0, {0x8 * (n + 1)}\n    "
    line += f"xvld $xr3, $t0, {0x8 * (n + 1)}\n    "
    line += f"{name} $xr0, $xr1, $xr2, $xr3\n"
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

def xd_rj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $xr0, $r20, {ui3}\n"
    return line

def vd_rj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $vr0, $r20, {ui2}\n"
    return line

def xd_rj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"ld.d $r20, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $xr0, $r20, {ui2}\n"
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

def _vd_rj_si12(name, n):
    line =  "la.local $t0, mem_k\n    "
    si12 = rand_imm(12, True)
    line += f"{name} $vr0, $t0, {0x8 * 4}\n"
    return line

def vd_rj_si11(name, n):
    line =  "la.local $t0, mem_k\n    "
    si11 = rand_imm(11, True)
    line += f"{name} $vr0, $t0, {si11}\n"
    return line

def vd_rj_si10(name, n):
    line =  "la.local $t0, mem_k\n    "
    si10 = rand_imm(10, True)
    line += f"{name} $vr0, $t0, {si10}\n"
    return line

def vd_rj_si9(name, n):
    line =  "la.local $t0, mem_k\n    "
    #si9 = rand_imm(9, True)
    si9 = 8
    line += f"{name} $vr0, $t0, {si9}\n"
    return line

def vd_rj_si8_idx(name, n):
    line =  "la.local $t1, mem_k\n    "
    line +=  "la.local $t0, out\n    "
    line += f"vld $vr1, $t1, {0x8 * 2}\n    "
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

def rd_xj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $r20, $xr0, {ui3}\n"
    return line

def rd_vj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $r20, $vr0, {ui2}\n"
    return line

def rd_xj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $r20, $xr0, {ui2}\n"
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

def xd_xj_ui8(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8}\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    ui8 = rand_imm(8, False)
    line += f"{name} $xr0, $xr1, {ui8}\n"
    return line

def vd_vj_ui7(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui7 = rand_imm(7, False)
    #print("ui7:  %d" %ui7)
    line += f"{name} $vr0, $vr1, {ui7}\n"
    return line

def xd_xj_ui7(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    line += f"xvld $xr1, $t0, {0x8 * (n + 1)}\n    "
    ui7 = rand_imm(7, False)
    line += f"{name} $xr0, $xr1, {ui7}\n"
    return line

def vd_vj_ui6(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui6 = rand_imm(6, False)
    line += f"{name} $vr0, $vr1, {ui6}\n"
    return line

def xd_xj_ui6(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    line += f"xvld $xr1, $t0, {0x8 * (n + 1)}\n    "
    ui6 = rand_imm(6, False)
    line += f"{name} $xr0, $xr1, {ui6}\n"
    return line

def vd_vj_ui5(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * 6}\n    "
    line += f"vld $vr1, $t0, {0x8 * (6 + 1)}\n    "
    #ui5 = rand_imm(5, False)
    ui5 = 0
    line += f"{name} $vr0, $vr1, {ui5}\n"
    return line

def xd_xj_ui5(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    line += f"xvld $xr1, $t0, {0x8 * (n + 1)}\n    "
    ui5 = rand_imm(5, False)
    line += f"{name} $xr0, $xr1, {ui5}\n"
    return line

def _xd_xj_ui5(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, 0x30\n    "
    line += f"xvld $xr1, $t0, 0x40\n    "
    line += f"{name} $xr0, $xr1, 0\n"
    return line

def vd_vj_si5(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    si5 = rand_imm(5, True)
    line += f"{name} $vr0, $vr1, {si5}\n"
    return line

def xd_xj_si5(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    line += f"xvld $xr1, $t0, {0x8 * (n + 1)}\n    "
    si5 = rand_imm(5, True)
    line += f"{name} $xr0, $xr1, {si5}\n"
    return line

def vd_vj_ui4(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui4 = rand_imm(4, False)
    line += f"{name} $vr0, $vr1, {ui4}\n"
    return line

def _vd_vj_ui4(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, 0\n    "
    #ui4 = rand_imm(4, False)
    ui4=7
    line += f"{name} $vr0, $vr1, {ui4}\n"
    return line

def _vd_vj_ui3(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, 0\n    "
    #ui4 = rand_imm(4, False)
    ui4=7
    line += f"{name} $vr0, $vr1, {ui4}\n"
    return line

def xd_xj_ui4(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    line += f"xvld $xr1, $t0, {0x8 * (n + 1)}\n    "
    ui4 = rand_imm(4, False)
    line += f"{name} $xr0, $xr1, {ui4}\n"
    return line

def vd_vj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"vld $vr1, $t0, {0x8 * (n + 1)}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $vr0, $vr1, {ui3}\n"
    return line

def xd_xj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, {0x8 * n}\n    "
    line += f"xvld $xr1, $t0, {0x8 * (n + 1)}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $xr0, $xr1, {ui3}\n"
    return line

def vd_vj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $vr0, $vr1, {ui2}\n"
    return line

def xd_xj_ui2(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    ui2 = rand_imm(2, False)
    line += f"{name} $xr0, $xr1, {ui2}\n"
    return line

def vd_vj_ui1(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $vr0, $vr1, {ui1}\n"
    return line

def xd_xj_ui1(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    ui1 = rand_imm(1, False)
    line += f"{name} $xr0, $xr1, {ui1}\n"
    return line

def vd_vj_s(name, n):
    line =  "la.local $t0, dataf\n    "
    line += f"vld $vr1, $t0, 0x8\n    "
    line += f"{name} $vr0, $vr1\n"
    return line

def vd_vj_d(name, n):
    line =  "la.local $t0, datad\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $vr1\n"
    return line

def vd_vj_vk_s(name, n):
    line =  "la.local $t0, dataf\n    "
    line += f"vld $vr1, $t0, {0x8 * 0}\n    "
    line += f"vld $vr2, $t0, {0x8 * (0+1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_vk_d(name, n):
    line =  "la.local $t0, datad\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"vld $vr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_vk_va_s(name, n):
    line =  "la.local $t0, dataf\n    "
    line += f"vld $vr1, $t0, {0x8 * 0}\n    "
    line += f"vld $vr2, $t0, {0x8 * (0 + 1)}\n    "
    line += f"vld $vr3, $t0, {0x8 * (0 + 2)}\n    "
    line += f"{name} $vr0, $vr1, $vr2, $vr3 \n"
    return line

def vd_vj_vk_va_d(name, n):
    line =  "la.local $t0, datad\n    "
    line += f"vld $vr1, $t0, {0x8 * 0}\n    "
    line += f"vld $vr2, $t0, {0x8 * 0}\n    "
    line += f"vld $vr3, $t0, {0x8 * 0}\n    "
    line += f"{name} $vr0, $vr1, $vr2, $vr3 \n"
    return line

def xd_xj_xk_s(name, n):
    line =  "la.local $t0, dataf\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    line += f"xvld $xr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $xr0, $xr1, $xr2\n"
    return line

def xd_xj_xk_d(name, n):
    line =  "la.local $t0, datad\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    line += f"xvld $xr2, $t0, {0x8 * (n+1)}\n    "
    line += f"{name} $xr0, $xr1, $xr2\n"
    return line

insts = [
###########Vector integer arithmetic insns
   # { "name": "vadd.b",           "func": vd_vj_vk      },
   # { "name": "vadd.h",           "func": vd_vj_vk      },
   # { "name": "vadd.w",           "func": vd_vj_vk      },
   # { "name": "vadd.d",           "func": vd_vj_vk      },
   # { "name": "vadd.q",           "func": vd_vj_vk      },
   # { "name": "vsub.b",           "func": vd_vj_vk      },
   # { "name": "vsub.h",           "func": vd_vj_vk      },
   # { "name": "vsub.w",           "func": vd_vj_vk      },
   # { "name": "vsub.d",           "func": vd_vj_vk      },
   # { "name": "vsub.q",           "func": vd_vj_vk      },
   # { "name": "xvadd.b",          "func": xd_xj_xk      },
   # { "name": "xvadd.h",          "func": xd_xj_xk      },
   # { "name": "xvadd.w",          "func": xd_xj_xk      },
   # { "name": "xvadd.d",          "func": xd_xj_xk      },
   # { "name": "xvadd.q",          "func": xd_xj_xk      },
   # { "name": "xvsub.b",          "func": xd_xj_xk      },
   # { "name": "xvsub.h",          "func": xd_xj_xk      },
   # { "name": "xvsub.w",          "func": xd_xj_xk      },
   # { "name": "xvsub.d",          "func": xd_xj_xk      },
   # { "name": "xvsub.q",          "func": xd_xj_xk      },
   # { "name": "vaddi.bu",         "func": vd_vj_ui5     },
   # { "name": "vaddi.hu",         "func": vd_vj_ui5     },
   # { "name": "vaddi.wu",         "func": vd_vj_ui5     },
   # { "name": "vaddi.du",         "func": vd_vj_ui5     },
   # { "name": "vsubi.bu",         "func": vd_vj_ui5     },
   # { "name": "vsubi.hu",         "func": vd_vj_ui5     },
   # { "name": "vsubi.wu",         "func": vd_vj_ui5     },
   # { "name": "vsubi.du",         "func": vd_vj_ui5     },
   # { "name": "xvaddi.bu",        "func": xd_xj_ui5     },
   # { "name": "xvaddi.hu",        "func": xd_xj_ui5     },
   # { "name": "xvaddi.wu",        "func": xd_xj_ui5     },
   # { "name": "xvaddi.du",        "func": xd_xj_ui5     },
   # { "name": "xvsubi.bu",        "func": xd_xj_ui5     },
   # { "name": "xvsubi.hu",        "func": xd_xj_ui5     },
   # { "name": "xvsubi.wu",        "func": xd_xj_ui5     },
   # { "name": "xvsubi.du",        "func": xd_xj_ui5     },
   # { "name": "vneg.b",           "func": vd_vj         },
   # { "name": "vneg.h",           "func": vd_vj         },
   # { "name": "vneg.w",           "func": vd_vj         },
   # { "name": "vneg.d",           "func": vd_vj         },
   # { "name": "xvneg.b",          "func": xd_xj         },
   # { "name": "xvneg.h",          "func": xd_xj         },
   # { "name": "xvneg.w",          "func": xd_xj         },
   # { "name": "xvneg.d",          "func": xd_xj         },
   # { "name": "vsadd.b",          "func": vd_vj_vk      },
   # { "name": "vsadd.h",          "func": vd_vj_vk      },
   # { "name": "vsadd.w",          "func": vd_vj_vk      },
   # { "name": "vsadd.d",          "func": vd_vj_vk      },
   # { "name": "vsadd.bu",         "func": vd_vj_vk      },
   # { "name": "vsadd.hu",         "func": vd_vj_vk      },
   # { "name": "vsadd.wu",         "func": vd_vj_vk      },
   # { "name": "vsadd.du",         "func": vd_vj_vk      },
   # { "name": "vssub.b",          "func": vd_vj_vk      },
   # { "name": "vssub.h",          "func": vd_vj_vk      },
   # { "name": "vssub.w",          "func": vd_vj_vk      },
   # { "name": "vssub.d",          "func": vd_vj_vk      },
   # { "name": "vssub.bu",         "func": vd_vj_vk      },
   # { "name": "vssub.hu",         "func": vd_vj_vk      },
   # { "name": "vssub.wu",         "func": vd_vj_vk      },
   # { "name": "vssub.du",         "func": vd_vj_vk      },
   # { "name": "xvsadd.b",         "func": xd_xj_xk      },
   # { "name": "xvsadd.h",         "func": xd_xj_xk      },
   # { "name": "xvsadd.w",         "func": xd_xj_xk      },
   # { "name": "xvsadd.d",         "func": xd_xj_xk      },
   # { "name": "xvsadd.bu",        "func": xd_xj_xk      },
   # { "name": "xvsadd.hu",        "func": xd_xj_xk      },
   # { "name": "xvsadd.wu",        "func": xd_xj_xk      },
   # { "name": "xvsadd.du",        "func": xd_xj_xk      },
   # { "name": "xvssub.b",         "func": xd_xj_xk      },
   # { "name": "xvssub.h",         "func": xd_xj_xk      },
   # { "name": "xvssub.w",         "func": xd_xj_xk      },
   # { "name": "xvssub.d",         "func": xd_xj_xk      },
   # { "name": "xvssub.bu",        "func": xd_xj_xk      },
   # { "name": "xvssub.hu",        "func": xd_xj_xk      },
   # { "name": "xvssub.wu",        "func": xd_xj_xk      },
   # { "name": "xvssub.du",        "func": xd_xj_xk      },
   # { "name": "vhaddw.h.b",       "func": vd_vj_vk      },
   # { "name": "vhaddw.w.h",       "func": vd_vj_vk      },
   # { "name": "vhaddw.d.w",       "func": vd_vj_vk      },
   # { "name": "vhaddw.q.d",       "func": vd_vj_vk      },
   # { "name": "vhsubw.h.b",       "func": vd_vj_vk      },
   # { "name": "vhsubw.w.h",       "func": vd_vj_vk      },
   # { "name": "vhsubw.d.w",       "func": vd_vj_vk      },
   # { "name": "vhsubw.q.d",       "func": vd_vj_vk      },
   # { "name": "vhaddw.hu.bu",     "func": vd_vj_vk      },
   # { "name": "vhaddw.wu.hu",     "func": vd_vj_vk      },
   # { "name": "vhaddw.du.wu",     "func": vd_vj_vk      },
   # { "name": "vhaddw.qu.du",     "func": vd_vj_vk      },
   # { "name": "vhsubw.hu.bu",     "func": vd_vj_vk      },
   # { "name": "vhsubw.wu.hu",     "func": vd_vj_vk      },
   # { "name": "vhsubw.du.wu",     "func": vd_vj_vk      },
   # { "name": "vhsubw.qu.du",     "func": vd_vj_vk      },
   # { "name": "xvhaddw.h.b",      "func": xd_xj_xk      },
   # { "name": "xvhaddw.w.h",      "func": xd_xj_xk      },
   # { "name": "xvhaddw.d.w",      "func": xd_xj_xk      },
   # { "name": "xvhaddw.q.d",      "func": xd_xj_xk      },
   # { "name": "xvhsubw.h.b",      "func": xd_xj_xk      },
   # { "name": "xvhsubw.w.h",      "func": xd_xj_xk      },
   # { "name": "xvhsubw.d.w",      "func": xd_xj_xk      },
   # { "name": "xvhsubw.q.d",      "func": xd_xj_xk      },
   # { "name": "xvhaddw.hu.bu",    "func": xd_xj_xk      },
   # { "name": "xvhaddw.wu.hu",    "func": xd_xj_xk      },
   # { "name": "xvhaddw.du.wu",    "func": xd_xj_xk      },
   # { "name": "xvhaddw.qu.du",    "func": xd_xj_xk      },
   # { "name": "xvhsubw.hu.bu",    "func": xd_xj_xk      },
   # { "name": "xvhsubw.wu.hu",    "func": xd_xj_xk      },
   # { "name": "xvhsubw.du.wu",    "func": xd_xj_xk      },
   # { "name": "xvhsubw.qu.du",    "func": xd_xj_xk      },
   # { "name": "vaddwev.h.b",      "func": vd_vj_vk      },
   # { "name": "vaddwev.w.h",      "func": vd_vj_vk      },
   # { "name": "vaddwev.d.w",      "func": vd_vj_vk      },
   # { "name": "vaddwev.q.d",      "func": vd_vj_vk      },
   # { "name": "vsubwev.h.b",      "func": vd_vj_vk      },
   # { "name": "vsubwev.w.h",      "func": vd_vj_vk      },
   # { "name": "vsubwev.d.w",      "func": vd_vj_vk      },
   # { "name": "vsubwev.q.d",      "func": vd_vj_vk      },
   # { "name": "vaddwod.h.b",      "func": vd_vj_vk      },
   # { "name": "vaddwod.w.h",      "func": vd_vj_vk      },
   # { "name": "vaddwod.d.w",      "func": vd_vj_vk      },
   # { "name": "vaddwod.q.d",      "func": vd_vj_vk      },
   # { "name": "vsubwod.h.b",      "func": vd_vj_vk      },
   # { "name": "vsubwod.w.h",      "func": vd_vj_vk      },
   # { "name": "vsubwod.d.w",      "func": vd_vj_vk      },
   # { "name": "vsubwod.q.d",      "func": vd_vj_vk      },
   # { "name": "vaddwev.h.bu",     "func": vd_vj_vk      },
   # { "name": "vaddwev.w.hu",     "func": vd_vj_vk      },
   # { "name": "vaddwev.d.wu",     "func": vd_vj_vk      },
   # { "name": "vaddwev.q.du",     "func": vd_vj_vk      },
   # { "name": "vsubwev.h.bu",     "func": vd_vj_vk      },
   # { "name": "vsubwev.w.hu",     "func": vd_vj_vk      },
   # { "name": "vsubwev.d.wu",     "func": vd_vj_vk      },
   # { "name": "vsubwev.q.du",     "func": vd_vj_vk      },
   # { "name": "vaddwod.h.bu",     "func": vd_vj_vk      },
   # { "name": "vaddwod.w.hu",     "func": vd_vj_vk      },
   # { "name": "vaddwod.d.wu",     "func": vd_vj_vk      },
   # { "name": "vaddwod.q.du",     "func": vd_vj_vk      },
   # { "name": "vsubwod.h.bu",     "func": vd_vj_vk      },
   # { "name": "vsubwod.w.hu",     "func": vd_vj_vk      },
   # { "name": "vsubwod.d.wu",     "func": vd_vj_vk      },
   # { "name": "vsubwod.q.du",     "func": vd_vj_vk      },
   # { "name": "xvaddwev.h.b",     "func": xd_xj_xk      },
   # { "name": "xvaddwev.w.h",     "func": xd_xj_xk      },
   # { "name": "xvaddwev.d.w",     "func": xd_xj_xk      },
   # { "name": "xvaddwev.q.d",     "func": xd_xj_xk      },
   # { "name": "xvsubwev.h.b",     "func": xd_xj_xk      },
   # { "name": "xvsubwev.w.h",     "func": xd_xj_xk      },
   # { "name": "xvsubwev.d.w",     "func": xd_xj_xk      },
   # { "name": "xvsubwev.q.d",     "func": xd_xj_xk      },
   # { "name": "xvaddwod.h.b",     "func": xd_xj_xk      },
   # { "name": "xvaddwod.w.h",     "func": xd_xj_xk      },
   # { "name": "xvaddwod.d.w",     "func": xd_xj_xk      },
   # { "name": "xvaddwod.q.d",     "func": xd_xj_xk      },
   # { "name": "xvsubwod.h.b",     "func": xd_xj_xk      },
   # { "name": "xvsubwod.w.h",     "func": xd_xj_xk      },
   # { "name": "xvsubwod.d.w",     "func": xd_xj_xk      },
   # { "name": "xvsubwod.q.d",     "func": xd_xj_xk      },
   # { "name": "xvaddwev.h.bu",    "func": xd_xj_xk      },
   # { "name": "xvaddwev.w.hu",    "func": xd_xj_xk      },
   # { "name": "xvaddwev.d.wu",    "func": xd_xj_xk      },
   # { "name": "xvaddwev.q.du",    "func": xd_xj_xk      },
   # { "name": "xvsubwev.h.bu",    "func": xd_xj_xk      },
   # { "name": "xvsubwev.w.hu",    "func": xd_xj_xk      },
   # { "name": "xvsubwev.d.wu",    "func": xd_xj_xk      },
   # { "name": "xvsubwev.q.du",    "func": xd_xj_xk      },
   # { "name": "xvaddwod.h.bu",    "func": xd_xj_xk      },
   # { "name": "xvaddwod.w.hu",    "func": xd_xj_xk      },
   # { "name": "xvaddwod.d.wu",    "func": xd_xj_xk      },
   # { "name": "xvaddwod.q.du",    "func": xd_xj_xk      },
   # { "name": "xvsubwod.h.bu",    "func": xd_xj_xk      },
   # { "name": "xvsubwod.w.hu",    "func": xd_xj_xk      },
   # { "name": "xvsubwod.d.wu",    "func": xd_xj_xk      },
   # { "name": "xvsubwod.q.du",    "func": xd_xj_xk      },
   # { "name": "vaddwev.h.bu.b",   "func": vd_vj_vk      },
   # { "name": "vaddwev.w.hu.h",   "func": vd_vj_vk      },
   # { "name": "vaddwev.d.wu.w",   "func": vd_vj_vk      },
   # { "name": "vaddwev.q.du.d",   "func": vd_vj_vk      },
   # { "name": "vaddwod.h.bu.b",   "func": vd_vj_vk      },
   # { "name": "vaddwod.w.hu.h",   "func": vd_vj_vk      },
   # { "name": "vaddwod.d.wu.w",   "func": vd_vj_vk      },
   # { "name": "vaddwod.q.du.d",   "func": vd_vj_vk      },
   # { "name": "xvaddwev.h.bu.b",  "func": xd_xj_xk      },
   # { "name": "xvaddwev.w.hu.h",  "func": xd_xj_xk      },
   # { "name": "xvaddwev.d.wu.w",  "func": xd_xj_xk      },
   # { "name": "xvaddwev.q.du.d",  "func": xd_xj_xk      },
   # { "name": "xvaddwod.h.bu.b",  "func": xd_xj_xk      },
   # { "name": "xvaddwod.w.hu.h",  "func": xd_xj_xk      },
   # { "name": "xvaddwod.d.wu.w",  "func": xd_xj_xk      },
   # { "name": "xvaddwod.q.du.d",  "func": xd_xj_xk      },
   # { "name": "vavg.b",           "func": vd_vj_vk      },
   # { "name": "vavg.h",           "func": vd_vj_vk      },
   # { "name": "vavg.w",           "func": vd_vj_vk      },
   # { "name": "vavg.d",           "func": vd_vj_vk      },
   # { "name": "vavg.bu",          "func": vd_vj_vk      },
   # { "name": "vavg.hu",          "func": vd_vj_vk      },
   # { "name": "vavg.wu",          "func": vd_vj_vk      },
   # { "name": "vavg.du",          "func": vd_vj_vk      },
   # { "name": "vavgr.b",          "func": vd_vj_vk      },
   # { "name": "vavgr.h",          "func": vd_vj_vk      },
   # { "name": "vavgr.w",          "func": vd_vj_vk      },
   # { "name": "vavgr.d",          "func": vd_vj_vk      },
   # { "name": "vavgr.bu",         "func": vd_vj_vk      },
   # { "name": "vavgr.hu",         "func": vd_vj_vk      },
   # { "name": "vavgr.wu",         "func": vd_vj_vk      },
   # { "name": "vavgr.du",         "func": vd_vj_vk      },
   # { "name": "xvavg.b",          "func": xd_xj_xk      },
   # { "name": "xvavg.h",          "func": xd_xj_xk      },
   # { "name": "xvavg.w",          "func": xd_xj_xk      },
   # { "name": "xvavg.d",          "func": xd_xj_xk      },
   # { "name": "xvavg.bu",         "func": xd_xj_xk      },
   # { "name": "xvavg.hu",         "func": xd_xj_xk      },
   # { "name": "xvavg.wu",         "func": xd_xj_xk      },
   # { "name": "xvavg.du",         "func": xd_xj_xk      },
   # { "name": "xvavgr.b",         "func": xd_xj_xk      },
   # { "name": "xvavgr.h",         "func": xd_xj_xk      },
   # { "name": "xvavgr.w",         "func": xd_xj_xk      },
   # { "name": "xvavgr.d",         "func": xd_xj_xk      },
   # { "name": "xvavgr.bu",        "func": xd_xj_xk      },
   # { "name": "xvavgr.hu",        "func": xd_xj_xk      },
   # { "name": "xvavgr.wu",        "func": xd_xj_xk      },
   # { "name": "xvavgr.du",        "func": xd_xj_xk      },
   # { "name": "vabsd.b",          "func": vd_vj_vk      },
   # { "name": "vabsd.h",          "func": vd_vj_vk      },
   # { "name": "vabsd.w",          "func": vd_vj_vk      },
   # { "name": "vabsd.d",          "func": vd_vj_vk      },
   # { "name": "vabsd.bu",         "func": vd_vj_vk      },
   # { "name": "vabsd.hu",         "func": vd_vj_vk      },
   # { "name": "vabsd.wu",         "func": vd_vj_vk      },
   # { "name": "vabsd.du",         "func": vd_vj_vk      },
   # { "name": "xvabsd.b",         "func": xd_xj_xk      },
   # { "name": "xvabsd.h",         "func": xd_xj_xk      },
   # { "name": "xvabsd.w",         "func": xd_xj_xk      },
   # { "name": "xvabsd.d",         "func": xd_xj_xk      },
   # { "name": "xvabsd.bu",        "func": xd_xj_xk      },
   # { "name": "xvabsd.hu",        "func": xd_xj_xk      },
   # { "name": "xvabsd.wu",        "func": xd_xj_xk      },
   # { "name": "xvabsd.du",        "func": xd_xj_xk      },
   # { "name": "vadda.b",          "func": vd_vj_vk      },
   # { "name": "vadda.h",          "func": vd_vj_vk      },
   # { "name": "vadda.w",          "func": vd_vj_vk      },
   # { "name": "vadda.d",          "func": vd_vj_vk      },
   # { "name": "xvadda.b",         "func": xd_xj_xk      },
   # { "name": "xvadda.h",         "func": xd_xj_xk      },
   # { "name": "xvadda.w",         "func": xd_xj_xk      },
   # { "name": "xvadda.d",         "func": xd_xj_xk      },
   # { "name": "vmax.b",           "func": vd_vj_vk      },
   # { "name": "vmax.h",           "func": vd_vj_vk      },
   # { "name": "vmax.w",           "func": vd_vj_vk      },
   # { "name": "vmax.d",           "func": vd_vj_vk      },
   # { "name": "vmax.bu",          "func": vd_vj_vk      },
   # { "name": "vmax.hu",          "func": vd_vj_vk      },
   # { "name": "vmax.wu",          "func": vd_vj_vk      },
   # { "name": "vmax.du",          "func": vd_vj_vk      },
   # { "name": "vmin.b",           "func": vd_vj_vk      },
   # { "name": "vmin.h",           "func": vd_vj_vk      },
   # { "name": "vmin.w",           "func": vd_vj_vk      },
   # { "name": "vmin.d",           "func": vd_vj_vk      },
   # { "name": "vmin.bu",          "func": vd_vj_vk      },
   # { "name": "vmin.hu",          "func": vd_vj_vk      },
   # { "name": "vmin.wu",          "func": vd_vj_vk      },
   # { "name": "vmin.du",          "func": vd_vj_vk      },
   # { "name": "xvmax.b",          "func": xd_xj_xk      },
   # { "name": "xvmax.h",          "func": xd_xj_xk      },
   # { "name": "xvmax.w",          "func": xd_xj_xk      },
   # { "name": "xvmax.d",          "func": xd_xj_xk      },
   # { "name": "xvmax.bu",         "func": xd_xj_xk      },
   # { "name": "xvmax.hu",         "func": xd_xj_xk      },
   # { "name": "xvmax.wu",         "func": xd_xj_xk      },
   # { "name": "xvmax.du",         "func": xd_xj_xk      },
   # { "name": "xvmin.b",          "func": xd_xj_xk      },
   # { "name": "xvmin.h",          "func": xd_xj_xk      },
   # { "name": "xvmin.w",          "func": xd_xj_xk      },
   # { "name": "xvmin.d",          "func": xd_xj_xk      },
   # { "name": "xvmin.bu",         "func": xd_xj_xk      },
   # { "name": "xvmin.hu",         "func": xd_xj_xk      },
   # { "name": "xvmin.wu",         "func": xd_xj_xk      },
   # { "name": "xvmin.du",         "func": xd_xj_xk      },
   # { "name": "vmaxi.b",          "func": vd_vj_si5     },
   # { "name": "vmaxi.h",          "func": vd_vj_si5     },
   # { "name": "vmaxi.w",          "func": vd_vj_si5     },
   # { "name": "vmaxi.d",          "func": vd_vj_si5     },
   # { "name": "vmaxi.bu",         "func": vd_vj_ui5     },
   # { "name": "vmaxi.hu",         "func": vd_vj_ui5     },
   # { "name": "vmaxi.wu",         "func": vd_vj_ui5     },
   # { "name": "vmaxi.du",         "func": vd_vj_ui5     },
   # { "name": "vmini.b",          "func": vd_vj_si5     },
   # { "name": "vmini.h",          "func": vd_vj_si5     },
   # { "name": "vmini.w",          "func": vd_vj_si5     },
   # { "name": "vmini.d",          "func": vd_vj_si5     },
   # { "name": "vmini.bu",         "func": vd_vj_ui5     },
   # { "name": "vmini.hu",         "func": vd_vj_ui5     },
   # { "name": "vmini.wu",         "func": vd_vj_ui5     },
   # { "name": "vmini.du",         "func": vd_vj_ui5     },
   # { "name": "xvmaxi.b",         "func": xd_xj_si5     },
   # { "name": "xvmaxi.h",         "func": xd_xj_si5     },
   # { "name": "xvmaxi.w",         "func": xd_xj_si5     },
   # { "name": "xvmaxi.d",         "func": xd_xj_si5     },
   # { "name": "xvmaxi.bu",        "func": xd_xj_ui5     },
   # { "name": "xvmaxi.hu",        "func": xd_xj_ui5     },
   # { "name": "xvmaxi.wu",        "func": xd_xj_ui5     },
   # { "name": "xvmaxi.du",        "func": xd_xj_ui5     },
   # { "name": "xvmini.b",         "func": xd_xj_si5     },
   # { "name": "xvmini.h",         "func": xd_xj_si5     },
   # { "name": "xvmini.w",         "func": xd_xj_si5     },
   # { "name": "xvmini.d",         "func": xd_xj_si5     },
   # { "name": "xvmini.bu",        "func": xd_xj_ui5     },
   # { "name": "xvmini.hu",        "func": xd_xj_ui5     },
   # { "name": "xvmini.wu",        "func": xd_xj_ui5     },
   # { "name": "xvmini.du",        "func": xd_xj_ui5     },
   # { "name": "vmul.b",           "func": vd_vj_vk      },
   # { "name": "vmul.h",           "func": vd_vj_vk      },
   # { "name": "vmul.w",           "func": vd_vj_vk      },
   # { "name": "vmul.d",           "func": vd_vj_vk      },
   # { "name": "vmuh.b",           "func": vd_vj_vk      },
   # { "name": "vmuh.h",           "func": vd_vj_vk      },
   # { "name": "vmuh.w",           "func": vd_vj_vk      },
   # { "name": "vmuh.d",           "func": vd_vj_vk      },
   # { "name": "vmuh.bu",          "func": vd_vj_vk      },
   # { "name": "vmuh.hu",          "func": vd_vj_vk      },
   # { "name": "vmuh.wu",          "func": vd_vj_vk      },
   # { "name": "vmuh.du",          "func": vd_vj_vk      },
   # { "name": "xvmul.b",          "func": xd_xj_xk      },
   # { "name": "xvmul.h",          "func": xd_xj_xk      },
   # { "name": "xvmul.w",          "func": xd_xj_xk      },
   # { "name": "xvmul.d",          "func": xd_xj_xk      },
   # { "name": "xvmuh.b",          "func": xd_xj_xk      },
   # { "name": "xvmuh.h",          "func": xd_xj_xk      },
   # { "name": "xvmuh.w",          "func": xd_xj_xk      },
   # { "name": "xvmuh.d",          "func": xd_xj_xk      },
   # { "name": "xvmuh.bu",         "func": xd_xj_xk      },
   # { "name": "xvmuh.hu",         "func": xd_xj_xk      },
   # { "name": "xvmuh.wu",         "func": xd_xj_xk      },
   # { "name": "xvmuh.du",         "func": xd_xj_xk      },
   # { "name": "vmulwev.h.b",      "func": vd_vj_vk      },
   # { "name": "vmulwev.w.h",      "func": vd_vj_vk      },
   # { "name": "vmulwev.d.w",      "func": vd_vj_vk      },
   # { "name": "vmulwev.q.d",      "func": vd_vj_vk      },
   # { "name": "vmulwod.h.b",      "func": vd_vj_vk      },
   # { "name": "vmulwod.w.h",      "func": vd_vj_vk      },
   # { "name": "vmulwod.d.w",      "func": vd_vj_vk      },
   # { "name": "vmulwod.q.d",      "func": vd_vj_vk      },
   # { "name": "vmulwev.h.bu",     "func": vd_vj_vk      },
   # { "name": "vmulwev.w.hu",     "func": vd_vj_vk      },
   # { "name": "vmulwev.d.wu",     "func": vd_vj_vk      },
   # { "name": "vmulwev.q.du",     "func": vd_vj_vk      },
   # { "name": "vmulwod.h.bu",     "func": vd_vj_vk      },
   # { "name": "vmulwod.w.hu",     "func": vd_vj_vk      },
   # { "name": "vmulwod.d.wu",     "func": vd_vj_vk      },
   # { "name": "vmulwod.q.du",     "func": vd_vj_vk      },
   # { "name": "xvmulwev.h.b",     "func": xd_xj_xk      },
   # { "name": "xvmulwev.w.h",     "func": xd_xj_xk      },
   # { "name": "xvmulwev.d.w",     "func": xd_xj_xk      },
   # { "name": "xvmulwev.q.d",     "func": xd_xj_xk      },
   # { "name": "xvmulwod.h.b",     "func": xd_xj_xk      },
   # { "name": "xvmulwod.w.h",     "func": xd_xj_xk      },
   # { "name": "xvmulwod.d.w",     "func": xd_xj_xk      },
   # { "name": "xvmulwod.q.d",     "func": xd_xj_xk      },
   # { "name": "xvmulwev.h.bu",    "func": xd_xj_xk      },
   # { "name": "xvmulwev.w.hu",    "func": xd_xj_xk      },
   # { "name": "xvmulwev.d.wu",    "func": xd_xj_xk      },
   # { "name": "xvmulwev.q.du",    "func": xd_xj_xk      },
   # { "name": "xvmulwod.h.bu",    "func": xd_xj_xk      },
   # { "name": "xvmulwod.w.hu",    "func": xd_xj_xk      },
   # { "name": "xvmulwod.d.wu",    "func": xd_xj_xk      },
   # { "name": "xvmulwod.q.du",    "func": xd_xj_xk      },
   # { "name": "vmulwev.h.bu.b",   "func": vd_vj_vk      },
   # { "name": "vmulwev.w.hu.h",   "func": vd_vj_vk      },
   # { "name": "vmulwev.d.wu.w",   "func": vd_vj_vk      },
   # { "name": "vmulwev.q.du.d",   "func": vd_vj_vk      }, #TODO
   # { "name": "vmulwod.h.bu.b",   "func": vd_vj_vk      },
   # { "name": "vmulwod.w.hu.h",   "func": vd_vj_vk      },
   # { "name": "vmulwod.d.wu.w",   "func": vd_vj_vk      },
   # { "name": "vmulwod.q.du.d",   "func": vd_vj_vk      }, #TODO
   # { "name": "xvmulwev.h.bu.b",  "func": xd_xj_xk      },
   # { "name": "xvmulwev.w.hu.h",  "func": xd_xj_xk      },
   # { "name": "xvmulwev.d.wu.w",  "func": xd_xj_xk      },
   # { "name": "xvmulwev.q.du.d",  "func": xd_xj_xk      }, #TODO
   # { "name": "xvmulwod.h.bu.b",  "func": xd_xj_xk      },
   # { "name": "xvmulwod.w.hu.h",  "func": xd_xj_xk      },
   # { "name": "xvmulwod.d.wu.w",  "func": xd_xj_xk      },
   # { "name": "xvmulwod.q.du.d",  "func": xd_xj_xk      }, #TODO
   # { "name": "vmadd.b",          "func": vd_vj_vk      },
   # { "name": "vmadd.h",          "func": vd_vj_vk      },
   # { "name": "vmadd.w",          "func": vd_vj_vk      },
   # { "name": "vmadd.d",          "func": vd_vj_vk      },
   # { "name": "vmsub.b",          "func": vd_vj_vk      },
   # { "name": "vmsub.h",          "func": vd_vj_vk      },
   # { "name": "vmsub.w",          "func": vd_vj_vk      },
   # { "name": "vmsub.d",          "func": vd_vj_vk      },
   # { "name": "xvmadd.b",         "func": xd_xj_xk      },
   # { "name": "xvmadd.h",         "func": xd_xj_xk      },
   # { "name": "xvmadd.w",         "func": xd_xj_xk      },
   # { "name": "xvmadd.d",         "func": xd_xj_xk      },
   # { "name": "xvmsub.b",         "func": xd_xj_xk      },
   # { "name": "xvmsub.h",         "func": xd_xj_xk      },
   # { "name": "xvmsub.w",         "func": xd_xj_xk      },
   # { "name": "xvmsub.d",         "func": xd_xj_xk      },
   # { "name": "vmaddwev.h.b",     "func": vd_vj_vk      },
   # { "name": "vmaddwev.w.h",     "func": vd_vj_vk      },
   # { "name": "vmaddwev.d.w",     "func": vd_vj_vk      },
   # { "name": "vmaddwev.q.d",     "func": vd_vj_vk      },
   # { "name": "vmaddwod.h.b",     "func": vd_vj_vk      },
   # { "name": "vmaddwod.w.h",     "func": vd_vj_vk      },
   # { "name": "vmaddwod.d.w",     "func": vd_vj_vk      },
   # { "name": "vmaddwod.q.d",     "func": vd_vj_vk      },
   # { "name": "vmaddwev.h.bu",    "func": vd_vj_vk      },
   # { "name": "vmaddwev.w.hu",    "func": vd_vj_vk      },
   # { "name": "vmaddwev.d.wu",    "func": vd_vj_vk      },
   # { "name": "vmaddwev.q.du",    "func": vd_vj_vk      },
   # { "name": "vmaddwod.h.bu",    "func": vd_vj_vk      },
   # { "name": "vmaddwod.w.hu",    "func": vd_vj_vk      },
   # { "name": "vmaddwod.d.wu",    "func": vd_vj_vk      },
   # { "name": "vmaddwod.q.du",    "func": vd_vj_vk      },
   # { "name": "xvmaddwev.h.b",    "func": xd_xj_xk      },
   # { "name": "xvmaddwev.w.h",    "func": xd_xj_xk      },
   # { "name": "xvmaddwev.d.w",    "func": xd_xj_xk      },
   # { "name": "xvmaddwev.q.d",    "func": xd_xj_xk      },
   # { "name": "xvmaddwod.h.b",    "func": xd_xj_xk      },
   # { "name": "xvmaddwod.w.h",    "func": xd_xj_xk      },
   # { "name": "xvmaddwod.d.w",    "func": xd_xj_xk      },
   # { "name": "xvmaddwod.q.d",    "func": xd_xj_xk      },
   # { "name": "xvmaddwev.h.bu",   "func": xd_xj_xk      },
   # { "name": "xvmaddwev.w.hu",   "func": xd_xj_xk      },
   # { "name": "xvmaddwev.d.wu",   "func": xd_xj_xk      },
   # { "name": "xvmaddwev.q.du",   "func": xd_xj_xk      },
   # { "name": "xvmaddwod.h.bu",   "func": xd_xj_xk      },
   # { "name": "xvmaddwod.w.hu",   "func": xd_xj_xk      },
   # { "name": "xvmaddwod.d.wu",   "func": xd_xj_xk      },
   # { "name": "xvmaddwod.q.du",   "func": xd_xj_xk      },
   # { "name": "vmaddwev.h.bu.b",  "func": vd_vj_vk      },
   # { "name": "vmaddwev.w.hu.h",  "func": vd_vj_vk      },
   # { "name": "vmaddwev.d.wu.w",  "func": vd_vj_vk      },
   # { "name": "vmaddwev.q.du.d",  "func": vd_vj_vk      }, #TODO
   # { "name": "vmaddwod.h.bu.b",  "func": vd_vj_vk      },
   # { "name": "vmaddwod.w.hu.h",  "func": vd_vj_vk      },
   # { "name": "vmaddwod.d.wu.w",  "func": vd_vj_vk      },
   # { "name": "vmaddwod.q.du.d",  "func": vd_vj_vk      }, #TODO
   # { "name": "xvmaddwev.h.bu.b", "func": xd_xj_xk      },
   # { "name": "xvmaddwev.w.hu.h", "func": xd_xj_xk      },
   # { "name": "xvmaddwev.d.wu.w", "func": xd_xj_xk      },
   # { "name": "xvmaddwev.q.du.d", "func": xd_xj_xk      }, #TODO
   # { "name": "xvmaddwod.h.bu.b", "func": xd_xj_xk      },
   # { "name": "xvmaddwod.w.hu.h", "func": xd_xj_xk      },
   # { "name": "xvmaddwod.d.wu.w", "func": xd_xj_xk      },
   # { "name": "xvmaddwod.q.du.d", "func": xd_xj_xk      }, #TODO
   # { "name": "vdiv.b",           "func": vd_vj_vk      },
   # { "name": "vdiv.h",           "func": vd_vj_vk      },
   # { "name": "vdiv.w",           "func": vd_vj_vk      },
   # { "name": "vdiv.d",           "func": vd_vj_vk      },
   # { "name": "vdiv.bu",          "func": vd_vj_vk      },
   # { "name": "vdiv.hu",          "func": vd_vj_vk      },
   # { "name": "vdiv.wu",          "func": vd_vj_vk      },
   # { "name": "vdiv.du",          "func": vd_vj_vk      },
   # { "name": "vmod.b",           "func": vd_vj_vk      },
   # { "name": "vmod.h",           "func": vd_vj_vk      },
   # { "name": "vmod.w",           "func": vd_vj_vk      },
   # { "name": "vmod.d",           "func": vd_vj_vk      },
   # { "name": "vmod.bu",          "func": vd_vj_vk      },
   # { "name": "vmod.hu",          "func": vd_vj_vk      },
   # { "name": "vmod.wu",          "func": vd_vj_vk      },
   # { "name": "vmod.du",          "func": vd_vj_vk      },
   # { "name": "xvdiv.b",          "func": xd_xj_xk      },
   # { "name": "xvdiv.h",          "func": xd_xj_xk      },
   # { "name": "xvdiv.w",          "func": xd_xj_xk      },
   # { "name": "xvdiv.d",          "func": xd_xj_xk      },
   # { "name": "xvdiv.bu",         "func": xd_xj_xk      },
   # { "name": "xvdiv.hu",         "func": xd_xj_xk      },
   # { "name": "xvdiv.wu",         "func": xd_xj_xk      },
   # { "name": "xvdiv.du",         "func": xd_xj_xk      },
   # { "name": "xvmod.b",          "func": xd_xj_xk      },
   # { "name": "xvmod.h",          "func": xd_xj_xk      },
   # { "name": "xvmod.w",          "func": xd_xj_xk      },
   # { "name": "xvmod.d",          "func": xd_xj_xk      },
   # { "name": "xvmod.bu",         "func": xd_xj_xk      },
   # { "name": "xvmod.hu",         "func": xd_xj_xk      },
   # { "name": "xvmod.wu",         "func": xd_xj_xk      },
   # { "name": "xvmod.du",         "func": xd_xj_xk      },
   # { "name": "vsat.b",           "func": vd_vj_ui3     },
   # { "name": "vsat.h",           "func": vd_vj_ui4     },
   # { "name": "vsat.w",           "func": vd_vj_ui5     },
   # { "name": "vsat.d",           "func": vd_vj_ui6     },
   # { "name": "vsat.bu",          "func": vd_vj_ui3     },
   # { "name": "vsat.hu",          "func": vd_vj_ui4     },
   # { "name": "vsat.wu",          "func": vd_vj_ui5     },
   # { "name": "vsat.du",          "func": vd_vj_ui6     },
   # { "name": "xvsat.b",          "func": xd_xj_ui3     },
   # { "name": "xvsat.h",          "func": xd_xj_ui4     },
   # { "name": "xvsat.w",          "func": xd_xj_ui5     },
   # { "name": "xvsat.d",          "func": xd_xj_ui6     },
   # { "name": "xvsat.bu",         "func": xd_xj_ui3     },
   # { "name": "xvsat.hu",         "func": xd_xj_ui4     },
   # { "name": "xvsat.wu",         "func": xd_xj_ui5     },
   # { "name": "xvsat.du",         "func": xd_xj_ui6     },
   # { "name": "vexth.h.b",        "func": vd_vj         },
   # { "name": "vexth.w.h",        "func": vd_vj         },
   # { "name": "vexth.d.w",        "func": vd_vj         },
   # { "name": "vexth.q.d",        "func": vd_vj         },
   # { "name": "vexth.hu.bu",      "func": vd_vj         },
   # { "name": "vexth.wu.hu",      "func": vd_vj         },
   # { "name": "vexth.du.wu",      "func": vd_vj         },
   # { "name": "vexth.qu.du",      "func": vd_vj         },
   # { "name": "xvexth.h.b",       "func": xd_xj         },
   # { "name": "xvexth.w.h",       "func": xd_xj         },
   # { "name": "xvexth.d.w",       "func": xd_xj         },
   # { "name": "xvexth.q.d",       "func": xd_xj         },
   # { "name": "xvexth.hu.bu",     "func": xd_xj         },
   # { "name": "xvexth.wu.hu",     "func": xd_xj         },
   # { "name": "xvexth.du.wu",     "func": xd_xj         },
   # { "name": "xvexth.qu.du",     "func": xd_xj         },
   # { "name": "vext2xv.h.b",      "func": xd_xj         },
   # { "name": "vext2xv.w.b",      "func": xd_xj         },
   # { "name": "vext2xv.d.b",      "func": xd_xj         },
   # { "name": "vext2xv.w.h",      "func": xd_xj         },
   # { "name": "vext2xv.d.h",      "func": xd_xj         },
   # { "name": "vext2xv.d.w",      "func": xd_xj         },
   # { "name": "vext2xv.hu.bu",    "func": xd_xj         },
   # { "name": "vext2xv.wu.bu",    "func": xd_xj         },
   # { "name": "vext2xv.du.bu",    "func": xd_xj         },
   # { "name": "vext2xv.wu.hu",    "func": xd_xj         },
   # { "name": "vext2xv.du.hu",    "func": xd_xj         },
   # { "name": "vext2xv.du.wu",    "func": xd_xj         },
   # { "name": "vsigncov.b",       "func": vd_vj_vk      },
   # { "name": "vsigncov.h",       "func": vd_vj_vk      },
   # { "name": "vsigncov.w",       "func": vd_vj_vk      },
   # { "name": "vsigncov.d",       "func": vd_vj_vk      },
   # { "name": "xvsigncov.b",      "func": xd_xj_xk      },
   # { "name": "xvsigncov.h",      "func": xd_xj_xk      },
   # { "name": "xvsigncov.w",      "func": xd_xj_xk      },
   # { "name": "xvsigncov.d",      "func": xd_xj_xk      },
   # { "name": "vmskltz.b",        "func": vd_vj         },
   # { "name": "vmskltz.h",        "func": vd_vj         },
   # { "name": "vmskltz.w",        "func": vd_vj         },
   # { "name": "vmskltz.d",        "func": vd_vj         },
   # { "name": "vmskgez.b",        "func": vd_vj         },
   # { "name": "vmsknz.b",         "func": vd_vj         },
   # { "name": "xvmskltz.b",       "func": xd_xj         },
   # { "name": "xvmskltz.h",       "func": xd_xj         },
   # { "name": "xvmskltz.w",       "func": xd_xj         },
   # { "name": "xvmskltz.d",       "func": xd_xj         },
   # { "name": "xvmskgez.b",       "func": xd_xj         },
   # { "name": "xvmsknz.b",        "func": xd_xj         },
   # { "name": "vldi",             "func": vd_si13       },
   # { "name": "xvldi",            "func": xd_si13       },

##############Vector bit operation insns
   # { "name": "vand.v",           "func": vd_vj_vk      },
   # { "name": "vor.v",            "func": vd_vj_vk      },
   # { "name": "vxor.v",           "func": vd_vj_vk      },
   # { "name": "vnor.v",           "func": vd_vj_vk      },
   # { "name": "vandn.v",          "func": vd_vj_vk      },
   # { "name": "vorn.v",           "func": vd_vj_vk      },
   # { "name": "xvand.v",          "func": xd_xj_xk      },
   # { "name": "xvor.v",           "func": xd_xj_xk      },
   # { "name": "xvxor.v",          "func": xd_xj_xk      },
   # { "name": "xvnor.v",          "func": xd_xj_xk      },
   # { "name": "xvandn.v",         "func": xd_xj_xk      },
   # { "name": "xvorn.v",          "func": xd_xj_xk      },
   # { "name": "vandi.b",          "func": vd_vj_ui8     },
   # { "name": "vori.b",           "func": vd_vj_ui8     },
   # { "name": "vxori.b",          "func": vd_vj_ui8     },
   # { "name": "vnori.b",          "func": vd_vj_ui8     },
   # { "name": "xvandi.b",         "func": xd_xj_ui8     },
   # { "name": "xvori.b",          "func": xd_xj_ui8     },
   # { "name": "xvxori.b",         "func": xd_xj_ui8     },
   # { "name": "xvnori.b",         "func": xd_xj_ui8     },
   # { "name": "vsll.b",           "func": vd_vj_vk      },
   # { "name": "vsll.h",           "func": vd_vj_vk      },
   # { "name": "vsll.w",           "func": vd_vj_vk      },
   # { "name": "vsll.d",           "func": vd_vj_vk      },
   # { "name": "vsrl.b",           "func": vd_vj_vk      },
   # { "name": "vsrl.h",           "func": vd_vj_vk      },
   # { "name": "vsrl.w",           "func": vd_vj_vk      },
   # { "name": "vsrl.d",           "func": vd_vj_vk      },
   # { "name": "vsra.b",           "func": vd_vj_vk      },
   # { "name": "vsra.h",           "func": vd_vj_vk      },
   # { "name": "vsra.w",           "func": vd_vj_vk      },
   # { "name": "vsra.d",           "func": vd_vj_vk      },
   # { "name": "vrotr.b",          "func": vd_vj_vk      },
   # { "name": "vrotr.h",          "func": vd_vj_vk      },
   # { "name": "vrotr.w",          "func": vd_vj_vk      },
   # { "name": "vrotr.d",          "func": vd_vj_vk      },
   # { "name": "xvsll.b",          "func": xd_xj_xk      },
   # { "name": "xvsll.h",          "func": xd_xj_xk      },
   # { "name": "xvsll.w",          "func": xd_xj_xk      },
   # { "name": "xvsll.d",          "func": xd_xj_xk      },
   # { "name": "xvsrl.b",          "func": xd_xj_xk      },
   # { "name": "xvsrl.h",          "func": xd_xj_xk      },
   # { "name": "xvsrl.w",          "func": xd_xj_xk      },
   # { "name": "xvsrl.d",          "func": xd_xj_xk      },
   # { "name": "xvsra.b",          "func": xd_xj_xk      },
   # { "name": "xvsra.h",          "func": xd_xj_xk      },
   # { "name": "xvsra.w",          "func": xd_xj_xk      },
   # { "name": "xvsra.d",          "func": xd_xj_xk      },
   # { "name": "xvrotr.b",         "func": xd_xj_xk      },
   # { "name": "xvrotr.h",         "func": xd_xj_xk      },
   # { "name": "xvrotr.w",         "func": xd_xj_xk      },
   # { "name": "xvrotr.d",         "func": xd_xj_xk      },
   # { "name": "vslli.b",          "func": vd_vj_ui3     },
   # { "name": "vslli.h",          "func": vd_vj_ui4     },
   # { "name": "vslli.w",          "func": vd_vj_ui5     },
   # { "name": "vslli.d",          "func": vd_vj_ui6     },
   # { "name": "vsrli.b",          "func": vd_vj_ui3     },
   # { "name": "vsrli.h",          "func": vd_vj_ui4     },
   # { "name": "vsrli.w",          "func": vd_vj_ui5     },
   # { "name": "vsrli.d",          "func": vd_vj_ui6     },
   # { "name": "vsrai.b",          "func": vd_vj_ui3     },
   # { "name": "vsrai.h",          "func": vd_vj_ui4     },
   # { "name": "vsrai.w",          "func": vd_vj_ui5     },
   # { "name": "vsrai.d",          "func": vd_vj_ui6     },
   # { "name": "vrotri.b",         "func": vd_vj_ui3     },
   # { "name": "vrotri.h",         "func": vd_vj_ui4     },
   # { "name": "vrotri.w",         "func": vd_vj_ui5     },
   # { "name": "vrotri.d",         "func": vd_vj_ui6     },
   # { "name": "xvslli.b",         "func": xd_xj_ui3     },
   # { "name": "xvslli.h",         "func": xd_xj_ui4     },
   # { "name": "xvslli.w",         "func": xd_xj_ui5     },
   # { "name": "xvslli.d",         "func": xd_xj_ui6     },
   # { "name": "xvsrli.b",         "func": xd_xj_ui3     },
   # { "name": "xvsrli.h",         "func": xd_xj_ui4     },
   # { "name": "xvsrli.w",         "func": xd_xj_ui5     },
   # { "name": "xvsrli.d",         "func": xd_xj_ui6     },
   # { "name": "xvsrai.b",         "func": xd_xj_ui3     },
   # { "name": "xvsrai.h",         "func": xd_xj_ui4     },
   # { "name": "xvsrai.w",         "func": xd_xj_ui5     },
   # { "name": "xvsrai.d",         "func": xd_xj_ui6     },
   # { "name": "xvrotri.b",        "func": xd_xj_ui3     },
   # { "name": "xvrotri.h",        "func": xd_xj_ui4     },
   # { "name": "xvrotri.w",        "func": xd_xj_ui5     },
   # { "name": "xvrotri.d",        "func": xd_xj_ui6     },
   # { "name": "vsllwil.h.b",      "func": vd_vj_ui3     },
   # { "name": "vsllwil.w.h",      "func": vd_vj_ui4     },
   # { "name": "vsllwil.d.w",      "func": vd_vj_ui5     },
   # { "name": "vextl.q.d",        "func": vd_vj         },
   # { "name": "vsllwil.hu.bu",    "func": vd_vj_ui3     },
   # { "name": "vsllwil.wu.hu",    "func": vd_vj_ui4     },
   # { "name": "vsllwil.du.wu",    "func": vd_vj_ui5     },
   # { "name": "vextl.qu.du",      "func": vd_vj         },
   # { "name": "xvsllwil.d.w",     "func": xd_xj_ui5     },
   # { "name": "xvextl.q.d",       "func": xd_xj         },
   # { "name": "xvsllwil.hu.bu",   "func": xd_xj_ui3     },
   # { "name": "xvsllwil.wu.hu",   "func": xd_xj_ui4     },
   # { "name": "xvsllwil.du.wu",   "func": xd_xj_ui5     },
   # { "name": "xvextl.qu.du",     "func": xd_xj         },
   # { "name": "vsrlr.b",          "func": vd_vj_vk      },
   # { "name": "vsrlr.h",          "func": vd_vj_vk      },
   # { "name": "vsrlr.w",          "func": vd_vj_vk      },
   # { "name": "vsrlr.d",          "func": vd_vj_vk      },
   # { "name": "vsrar.b",          "func": vd_vj_vk      },
   # { "name": "vsrar.h",          "func": vd_vj_vk      },
   # { "name": "vsrar.w",          "func": vd_vj_vk      },
   # { "name": "vsrar.d",          "func": vd_vj_vk      },
   # { "name": "xvsrlr.b",         "func": xd_xj_xk      },
   # { "name": "xvsrlr.h",         "func": xd_xj_xk      },
   # { "name": "xvsrlr.w",         "func": xd_xj_xk      },
   # { "name": "xvsrlr.d",         "func": xd_xj_xk      },
   # { "name": "xvsrar.b",         "func": xd_xj_xk      },
   # { "name": "xvsrar.h",         "func": xd_xj_xk      },
   # { "name": "xvsrar.w",         "func": xd_xj_xk      },
   # { "name": "xvsrar.d",         "func": xd_xj_xk      },
   # { "name": "vsrlri.b",         "func": vd_vj_ui2     },
   # { "name": "vsrlri.h",         "func": vd_vj_ui4     },
   # { "name": "vsrlri.w",         "func": vd_vj_ui5     },
   # { "name": "vsrlri.d",         "func": vd_vj_ui6     },
   # { "name": "vsrari.b",         "func": vd_vj_ui3     },
   # { "name": "vsrari.h",         "func": vd_vj_ui4     },
   # { "name": "vsrari.w",         "func": vd_vj_ui5     },
   # { "name": "vsrari.d",         "func": vd_vj_ui6     },
   # { "name": "xvsrlri.b",        "func": xd_xj_ui3     },
   # { "name": "xvsrlri.h",        "func": xd_xj_ui4     },
   # { "name": "xvsrlri.w",        "func": xd_xj_ui5     },
   # { "name": "xvsrlri.d",        "func": xd_xj_ui6     },
   # { "name": "xvsrari.b",        "func": xd_xj_ui3     },
   # { "name": "xvsrari.h",        "func": xd_xj_ui4     },
   # { "name": "xvsrari.w",        "func": xd_xj_ui5     },
   # { "name": "xvsrari.d",        "func": xd_xj_ui6     },
   # { "name": "vsrln.b.h",        "func": vd_vj_vk      },
   # { "name": "vsrln.h.w",        "func": vd_vj_vk      },
   # { "name": "vsrln.w.d",        "func": vd_vj_vk      },
   # { "name": "vsran.b.h",        "func": vd_vj_vk      },
   # { "name": "vsran.h.w",        "func": vd_vj_vk      },
   # { "name": "vsran.w.d",        "func": vd_vj_vk      },
   # { "name": "xvsrln.b.h",       "func": xd_xj_xk      },
   # { "name": "xvsrln.h.w",       "func": xd_xj_xk      },
   # { "name": "xvsrln.w.d",       "func": xd_xj_xk      },
   # { "name": "xvsran.b.h",       "func": xd_xj_xk      },
   # { "name": "xvsran.h.w",       "func": xd_xj_xk      },
   # { "name": "xvsran.w.d",       "func": xd_xj_xk      },
   # { "name": "vsrlni.b.h",       "func": vd_vj_ui4     },
   # { "name": "vsrlni.h.w",       "func": vd_vj_ui5     },
   # { "name": "vsrlni.w.d",       "func": vd_vj_ui6     },
   # { "name": "vsrlni.d.q",       "func": vd_vj_ui7     },
   # { "name": "vsrani.b.h",       "func": vd_vj_ui4     },
   # { "name": "vsrani.h.w",       "func": vd_vj_ui5     },
   # { "name": "vsrani.w.d",       "func": vd_vj_ui6     },
   # { "name": "vsrani.d.q",       "func": vd_vj_ui7     },
   # { "name": "xvsrlni.b.h",      "func": xd_xj_ui4     },
   # { "name": "xvsrlni.h.w",      "func": xd_xj_ui5     },
   # { "name": "xvsrlni.w.d",      "func": xd_xj_ui6     },
   # { "name": "xvsrlni.d.q",      "func": xd_xj_ui7     },
   # { "name": "xvsrani.b.h",      "func": xd_xj_ui4     },
   # { "name": "xvsrani.h.w",      "func": xd_xj_ui5     },
   # { "name": "xvsrani.w.d",      "func": xd_xj_ui6     },
   # { "name": "xvsrani.d.q",      "func": xd_xj_ui7     },
   # { "name": "vsrlrn.b.h",       "func": vd_vj_vk      },
   # { "name": "vsrlrn.h.w",       "func": vd_vj_vk      },
   # { "name": "vsrlrn.w.d",       "func": vd_vj_vk      },
   # { "name": "vsrarn.b.h",       "func": vd_vj_vk      },
   # { "name": "vsrarn.h.w",       "func": vd_vj_vk      },
   # { "name": "vsrarn.w.d",       "func": vd_vj_vk      },
   # { "name": "xvsrlrn.b.h",      "func": xd_xj_xk      },
   # { "name": "xvsrlrn.h.w",      "func": xd_xj_xk      },
   # { "name": "xvsrlrn.w.d",      "func": xd_xj_xk      },
   # { "name": "xvsrarn.b.h",      "func": xd_xj_xk      },
   # { "name": "xvsrarn.h.w",      "func": xd_xj_xk      },
   # { "name": "xvsrarn.w.d",      "func": xd_xj_xk      },
   # { "name": "vsrlrni.b.h",      "func": vd_vj_ui4     },
   # { "name": "vsrlrni.h.w",      "func": vd_vj_ui5     },
   # { "name": "vsrlrni.w.d",      "func": vd_vj_ui6     },
   # { "name": "vsrlrni.d.q",      "func": vd_vj_ui7     },
   # { "name": "vsrarni.b.h",      "func": vd_vj_ui4     },
   # { "name": "vsrarni.h.w",      "func": vd_vj_ui5     },
   # { "name": "vsrarni.w.d",      "func": vd_vj_ui6     },
   # { "name": "vsrarni.d.q",      "func": vd_vj_ui7     },
   # { "name": "xvsrlrni.b.h",     "func": xd_xj_ui4     },
   # { "name": "xvsrlrni.h.w",     "func": xd_xj_ui5     },
   # { "name": "xvsrlrni.w.d",     "func": xd_xj_ui6     },
   # { "name": "xvsrlrni.d.q",     "func": xd_xj_ui7     },
   # { "name": "xvsrarni.b.h",     "func": xd_xj_ui4     },
   # { "name": "xvsrarni.h.w",     "func": xd_xj_ui5     },
   # { "name": "xvsrarni.w.d",     "func": xd_xj_ui6     },
   # { "name": "xvsrarni.d.q",     "func": xd_xj_ui7     },

#TODO
   # { "name": "vssrln.b.h",       "func": vd_vj_vk      },
   # { "name": "vssrln.h.w",       "func": vd_vj_vk      },
   # { "name": "vssrln.w.d",       "func": vd_vj_vk      },
   # { "name": "vssran.b.h",       "func": vd_vj_vk      },
   # { "name": "vssran.h.w",       "func": vd_vj_vk      },
   # { "name": "vssran.w.d",       "func": vd_vj_vk      },
   # { "name": "vssrln.bu.h",      "func": vd_vj_vk      },
   # { "name": "vssrln.hu.w",      "func": vd_vj_vk      },
   # { "name": "vssrln.wu.d",      "func": vd_vj_vk      },
   # { "name": "vssran.bu.h",      "func": vd_vj_vk      },
   # { "name": "vssran.hu.w",      "func": vd_vj_vk      },
   # { "name": "vssran.wu.d",      "func": vd_vj_vk      },
   # { "name": "xvssrln.b.h",      "func": xd_xj_xk      },
   # { "name": "xvssrln.h.w",      "func": xd_xj_xk      },
   # { "name": "xvssrln.w.d",      "func": xd_xj_xk      },
   # { "name": "xvssran.b.h",      "func": xd_xj_xk      },
   # { "name": "xvssran.h.w",      "func": xd_xj_xk      },
   # { "name": "xvssran.w.d",      "func": xd_xj_xk      },
   # { "name": "xvssrln.bu.h",     "func": xd_xj_xk      },
   # { "name": "xvssrln.hu.w",     "func": xd_xj_xk      },
   # { "name": "xvssrln.wu.d",     "func": xd_xj_xk      },
   # { "name": "xvssran.bu.h",     "func": xd_xj_xk      },
   # { "name": "xvssran.hu.w",     "func": xd_xj_xk      },
   # { "name": "xvssran.wu.d",     "func": xd_xj_xk      },
   # { "name": "vssrlni.b.h",      "func": vd_vj_ui4     },
   # { "name": "vssrlni.h.w",      "func": vd_vj_ui5     },
   # { "name": "vssrlni.w.d",      "func": vd_vj_ui6     },
   # { "name": "vssrlni.d.q",      "func": vd_vj_ui7     },
   # { "name": "vssrani.b.h",      "func": vd_vj_ui4     },
   # { "name": "vssrani.h.w",      "func": vd_vj_ui5     },
   # { "name": "vssrani.w.d",      "func": vd_vj_ui6     },
   # { "name": "vssrani.d.q",      "func": vd_vj_ui7     },
   # { "name": "vssrlni.bu.h",     "func": vd_vj_ui4     },
   # { "name": "vssrlni.hu.w",     "func": vd_vj_ui5     },
   # { "name": "vssrlni.wu.d",     "func": vd_vj_ui6     },
   # { "name": "vssrlni.du.q",     "func": vd_vj_ui7     },
   # { "name": "vssrani.bu.h",     "func": vd_vj_ui4     },
   # { "name": "vssrani.hu.w",     "func": vd_vj_ui5     },
   # { "name": "vssrani.wu.d",     "func": vd_vj_ui6     },
   # { "name": "vssrani.du.q",     "func": vd_vj_ui7     },
   # { "name": "xvssrlni.b.h",     "func": xd_xj_ui4     },
   # { "name": "xvssrlni.h.w",     "func": xd_xj_ui5     },
   # { "name": "xvssrlni.w.d",     "func": xd_xj_ui6     },
   # { "name": "xvssrlni.d.q",     "func": xd_xj_ui7     },
   # { "name": "xvssrani.b.h",     "func": xd_xj_ui4     },
   # { "name": "xvssrani.h.w",     "func": xd_xj_ui5     },
   # { "name": "xvssrani.w.d",     "func": xd_xj_ui6     },
   # { "name": "xvssrani.d.q",     "func": xd_xj_ui7     },
   # { "name": "xvssrlni.bu.h",    "func": xd_xj_ui4     },
   # { "name": "xvssrlni.hu.w",    "func": xd_xj_ui5     },
   # { "name": "xvssrlni.wu.d",    "func": xd_xj_ui6     },
   # { "name": "xvssrlni.du.q",    "func": xd_xj_ui7     },
   # { "name": "xvssrani.bu.h",    "func": xd_xj_ui4     },
   # { "name": "xvssrani.hu.w",    "func": xd_xj_ui5     },
   # { "name": "xvssrani.wu.d",    "func": xd_xj_ui6     },
   # { "name": "xvssrani.du.q",    "func": xd_xj_ui7     },
   # { "name": "vssrlrn.b.h",      "func": vd_vj_vk      },
   # { "name": "vssrlrn.h.w",      "func": vd_vj_vk      },
   # { "name": "vssrlrn.w.d",      "func": vd_vj_vk      },
   # { "name": "vssrarn.b.h",      "func": vd_vj_vk      },
   # { "name": "vssrarn.h.w",      "func": vd_vj_vk      },
   # { "name": "vssrarn.w.d",      "func": vd_vj_vk      },
   # { "name": "vssrlrn.bu.h",     "func": vd_vj_vk      },
   # { "name": "vssrlrn.hu.w",     "func": vd_vj_vk      },
   # { "name": "vssrlrn.wu.d",     "func": vd_vj_vk      },
   # { "name": "vssrarn.bu.h",     "func": vd_vj_vk      },
   # { "name": "vssrarn.hu.w",     "func": vd_vj_vk      },
   # { "name": "vssrarn.wu.d",     "func": vd_vj_vk      },
   # { "name": "xvssrlrn.b.h",     "func": xd_xj_xk      },
   # { "name": "xvssrlrn.h.w",     "func": xd_xj_xk      },
   # { "name": "xvssrlrn.w.d",     "func": xd_xj_xk      },
   # { "name": "xvssrarn.b.h",     "func": xd_xj_xk      },
   # { "name": "xvssrarn.h.w",     "func": xd_xj_xk      },
   # { "name": "xvssrarn.w.d",     "func": xd_xj_xk      },
   # { "name": "xvssrlrn.bu.h",    "func": xd_xj_xk      },
   # { "name": "xvssrlrn.hu.w",    "func": xd_xj_xk      },
   # { "name": "xvssrlrn.wu.d",    "func": xd_xj_xk      },
   # { "name": "xvssrarn.bu.h",    "func": xd_xj_xk      },
   # { "name": "xvssrarn.hu.w",    "func": xd_xj_xk      },
   # { "name": "xvssrarn.wu.d",    "func": xd_xj_xk      },
   # { "name": "vssrlrni.b.h",     "func": vd_vj_ui4     },
   # { "name": "vssrlrni.h.w",     "func": vd_vj_ui5     },
   # { "name": "vssrlrni.w.d",     "func": vd_vj_ui6     },
   # { "name": "vssrlrni.d.q",     "func": vd_vj_ui7     },
   # { "name": "vssrarni.b.h",     "func": vd_vj_ui4     },
   # { "name": "vssrarni.h.w",     "func": vd_vj_ui5     },
   # { "name": "vssrarni.w.d",     "func": vd_vj_ui6     },
   # { "name": "vssrarni.d.q",     "func": vd_vj_ui7     },
   # { "name": "vssrlrni.bu.h",    "func": vd_vj_ui4     },
   # { "name": "vssrlrni.hu.w",    "func": vd_vj_ui5     },
   # { "name": "vssrlrni.wu.d",    "func": vd_vj_ui6     },
   # { "name": "vssrlrni.du.q",    "func": vd_vj_ui7     },
   # { "name": "vssrarni.bu.h",    "func": vd_vj_ui4     },
   # { "name": "vssrarni.hu.w",    "func": vd_vj_ui5     },
   # { "name": "vssrarni.wu.d",    "func": vd_vj_ui6     },
   # { "name": "vssrarni.du.q",    "func": vd_vj_ui7     },
   # { "name": "xvssrlrni.b.h",    "func": xd_xj_ui4     },
   # { "name": "xvssrlrni.h.w",    "func": xd_xj_ui5     },
   # { "name": "xvssrlrni.w.d",    "func": xd_xj_ui6     },
   # { "name": "xvssrlrni.d.q",    "func": xd_xj_ui7     },
   # { "name": "xvssrarni.b.h",    "func": xd_xj_ui4     },
   # { "name": "xvssrarni.h.w",    "func": xd_xj_ui5     },
   # { "name": "xvssrarni.w.d",    "func": xd_xj_ui6     },
   # { "name": "xvssrarni.d.q",    "func": xd_xj_ui7     },
   # { "name": "xvssrlrni.bu.h",   "func": xd_xj_ui4     },
   # { "name": "xvssrlrni.hu.w",   "func": xd_xj_ui5     },
   # { "name": "xvssrlrni.wu.d",   "func": xd_xj_ui6     },
   # { "name": "xvssrlrni.du.q",   "func": xd_xj_ui7     },
   # { "name": "xvssrarni.bu.h",   "func": xd_xj_ui4     },
   # { "name": "xvssrarni.hu.w",   "func": xd_xj_ui5     },
   # { "name": "xvssrarni.wu.d",   "func": xd_xj_ui6     },
   # { "name": "xvssrarni.du.q",   "func": xd_xj_ui7     },

    { "name": "vclo.b",           "func": vd_vj         },
    { "name": "vclo.h",           "func": vd_vj         },
    { "name": "vclo.w",           "func": vd_vj         },
    { "name": "vclo.d",           "func": vd_vj         },
    { "name": "vclz.b",           "func": vd_vj         },
    { "name": "vclz.h",           "func": vd_vj         },
    { "name": "vclz.w",           "func": vd_vj         },
    { "name": "vclz.d",           "func": vd_vj         },
    { "name": "vpcnt.b",          "func": vd_vj         },
    { "name": "vpcnt.h",          "func": vd_vj         },
    { "name": "vpcnt.w",          "func": vd_vj         },
    { "name": "vpcnt.d",          "func": vd_vj         },
    { "name": "xvclo.b",          "func": xd_xj         },
    { "name": "xvclo.h",          "func": xd_xj         },
    { "name": "xvclo.w",          "func": xd_xj         },
    { "name": "xvclo.d",          "func": xd_xj         },
    { "name": "xvclz.b",          "func": xd_xj         },
    { "name": "xvclz.h",          "func": xd_xj         },
    { "name": "xvclz.w",          "func": xd_xj         },
    { "name": "xvclz.d",          "func": xd_xj         },
    { "name": "xvpcnt.b",         "func": xd_xj         },
    { "name": "xvpcnt.h",         "func": xd_xj         },
    { "name": "xvpcnt.w",         "func": xd_xj         },
    { "name": "xvpcnt.d",         "func": xd_xj         },
    { "name": "vbitclr.b",        "func": vd_vj_vk      },
    { "name": "vbitclr.h",        "func": vd_vj_vk      },
    { "name": "vbitclr.w",        "func": vd_vj_vk      },
    { "name": "vbitclr.d",        "func": vd_vj_vk      },
    { "name": "vbitset.b",        "func": vd_vj_vk      },
    { "name": "vbitset.h",        "func": vd_vj_vk      },
    { "name": "vbitset.w",        "func": vd_vj_vk      },
    { "name": "vbitset.d",        "func": vd_vj_vk      },
    { "name": "vbitrev.b",        "func": vd_vj_vk      },
    { "name": "vbitrev.h",        "func": vd_vj_vk      },
    { "name": "vbitrev.w",        "func": vd_vj_vk      },
    { "name": "vbitrev.d",        "func": vd_vj_vk      },
    { "name": "xvbitclr.b",       "func": xd_xj_xk      },
    { "name": "xvbitclr.h",       "func": xd_xj_xk      },
    { "name": "xvbitclr.w",       "func": xd_xj_xk      },
    { "name": "xvbitclr.d",       "func": xd_xj_xk      },
    { "name": "xvbitset.b",       "func": xd_xj_xk      },
    { "name": "xvbitset.h",       "func": xd_xj_xk      },
    { "name": "xvbitset.w",       "func": xd_xj_xk      },
    { "name": "xvbitset.d",       "func": xd_xj_xk      },
    { "name": "xvbitrev.b",       "func": xd_xj_xk      },
    { "name": "xvbitrev.h",       "func": xd_xj_xk      },
    { "name": "xvbitrev.w",       "func": xd_xj_xk      },
    { "name": "xvbitrev.d",       "func": xd_xj_xk      },
    { "name": "vbitclri.b",       "func": vd_vj_ui3     },
    { "name": "vbitclri.h",       "func": vd_vj_ui4     },
    { "name": "vbitclri.w",       "func": vd_vj_ui5     },
    { "name": "vbitclri.d",       "func": vd_vj_ui6     },
    { "name": "vbitseti.b",       "func": vd_vj_ui3     },
    { "name": "vbitseti.h",       "func": vd_vj_ui4     },
    { "name": "vbitseti.w",       "func": vd_vj_ui5     },
    { "name": "vbitseti.d",       "func": vd_vj_ui6     },
    { "name": "vbitrevi.b",       "func": vd_vj_ui3     },
    { "name": "vbitrevi.h",       "func": vd_vj_ui4     },
    { "name": "vbitrevi.w",       "func": vd_vj_ui5     },
    { "name": "vbitrevi.d",       "func": vd_vj_ui6     },
    { "name": "xvbitclri.b",      "func": xd_xj_ui3     },
    { "name": "xvbitclri.h",      "func": xd_xj_ui4     },
    { "name": "xvbitclri.w",      "func": xd_xj_ui5     },
    { "name": "xvbitclri.d",      "func": xd_xj_ui6     },
    { "name": "xvbitseti.b",      "func": xd_xj_ui3     },
    { "name": "xvbitseti.h",      "func": xd_xj_ui4     },
    { "name": "xvbitseti.w",      "func": xd_xj_ui5     },
    { "name": "xvbitseti.d",      "func": xd_xj_ui6     },
    { "name": "xvbitrevi.b",      "func": xd_xj_ui3     },
    { "name": "xvbitrevi.h",      "func": xd_xj_ui4     },
    { "name": "xvbitrevi.w",      "func": xd_xj_ui5     },
    { "name": "xvbitrevi.d",      "func": xd_xj_ui6     },

##############Vector String Processing insns
   # { "name": "vfrstp.b",         "func": vd_vj_vk      }, #bad
   # { "name": "vfrstp.h",         "func": vd_vj_vk      }, #bad
   # { "name": "xvfrstp.b",        "func": xd_xj_xk      }, #bad
   # { "name": "xvfrstp.h",        "func": xd_xj_xk      }, #bad
   # { "name": "vfrstpi.b",        "func": vd_vj_ui5     },
   # { "name": "vfrstpi.h",        "func": vd_vj_ui5     },
   # { "name": "xvfrstpi.b",       "func": xd_xj_ui5     },
   # { "name": "xvfrstpi.h",       "func": xd_xj_ui5     },

###########Vector Floating-point Operation insns
   # { "name": "vfadd.s",          "func": vd_vj_vk_s    },
   # { "name": "vfadd.d",          "func": vd_vj_vk_d    },
   # { "name": "vfsub.s",          "func": vd_vj_vk_s    },
   # { "name": "vfsub.d",          "func": vd_vj_vk_d    },
   # { "name": "vfmul.s",          "func": vd_vj_vk_s    },
   # { "name": "vfmul.d",          "func": vd_vj_vk_d    },
   # { "name": "vfdiv.s",          "func": vd_vj_vk_s    },
   # { "name": "vfdiv.d",          "func": vd_vj_vk_d    },

   # { "name": "vfmadd.s",         "func": vd_vj_vk_va_s }, #bad
   # { "name": "vfmadd.d",         "func": vd_vj_vk_va_d }, #bad
   # { "name": "vfmax.s",          "func": vd_vj_vk_s    },
   # { "name": "vfmax.d",          "func": vd_vj_vk_d    },
   # { "name": "vfmin.s",          "func": vd_vj_vk_s    },
   # { "name": "vfmin.d",          "func": vd_vj_vk_d    },
   # { "name": "vflogb.s",         "func": vd_vj_s       },

################Vector comparison and selection insns 
   # { "name": "vseq.b",           "func": vd_vj_vk      },
   # { "name": "vseq.h",           "func": vd_vj_vk      },
   # { "name": "vseq.w",           "func": vd_vj_vk      },
   # { "name": "vseq.d",           "func": vd_vj_vk      },
   # { "name": "vseqi.b",          "func": vd_vj_si5     },
   # { "name": "vseqi.h",          "func": vd_vj_si5     },
   # { "name": "vseqi.w",          "func": vd_vj_si5     },
   # { "name": "vseqi.d",          "func": vd_vj_si5     },
   # { "name": "xvseq.b",          "func": xd_xj_xk      },
   # { "name": "xvseq.h",          "func": xd_xj_xk      },
   # { "name": "xvseq.w",          "func": xd_xj_xk      },
   # { "name": "xvseq.d",          "func": xd_xj_xk      },
   # { "name": "xvseqi.b",         "func": xd_xj_si5     },
   # { "name": "xvseqi.h",         "func": xd_xj_si5     },
   # { "name": "xvseqi.w",         "func": xd_xj_si5     },
   # { "name": "xvseqi.d",         "func": xd_xj_si5     },
   # { "name": "vsle.b",           "func": vd_vj_vk      },
   # { "name": "vsle.h",           "func": vd_vj_vk      },
   # { "name": "vsle.w",           "func": vd_vj_vk      },
   # { "name": "vsle.d",           "func": vd_vj_vk      },
   # { "name": "vslei.b",          "func": vd_vj_si5     },
   # { "name": "vslei.h",          "func": vd_vj_si5     },
   # { "name": "vslei.w",          "func": vd_vj_si5     },
   # { "name": "vslei.d",          "func": vd_vj_si5     },
   # { "name": "vsle.bu",          "func": vd_vj_vk      },
   # { "name": "vsle.hu",          "func": vd_vj_vk      },
   # { "name": "vsle.wu",          "func": vd_vj_vk      },
   # { "name": "vsle.du",          "func": vd_vj_vk      },
   # { "name": "vslei.bu",         "func": vd_vj_ui5     },
   # { "name": "vslei.hu",         "func": vd_vj_ui5     },
   # { "name": "vslei.wu",         "func": vd_vj_ui5     },
   # { "name": "vslei.du",         "func": vd_vj_ui5     },
   # { "name": "xvsle.b",          "func": xd_xj_xk      },
   # { "name": "xvsle.h",          "func": xd_xj_xk      },
   # { "name": "xvsle.w",          "func": xd_xj_xk      },
   # { "name": "xvsle.d",          "func": xd_xj_xk      },
   # { "name": "xvslei.b",         "func": xd_xj_si5     },
   # { "name": "xvslei.h",         "func": xd_xj_si5     },
   # { "name": "xvslei.w",         "func": xd_xj_si5     },
   # { "name": "xvslei.d",         "func": xd_xj_si5     },
   # { "name": "xvsle.bu",         "func": xd_xj_xk      },
   # { "name": "xvsle.hu",         "func": xd_xj_xk      },
   # { "name": "xvsle.wu",         "func": xd_xj_xk      },
   # { "name": "xvsle.du",         "func": xd_xj_xk      },
   # { "name": "xvslei.bu",        "func": xd_xj_ui5     },
   # { "name": "xvslei.hu",        "func": xd_xj_ui5     },
   # { "name": "xvslei.wu",        "func": xd_xj_ui5     },
   # { "name": "xvslei.du",        "func": xd_xj_ui5     },
   # { "name": "vslt.b",           "func": vd_vj_vk      },
   # { "name": "vslt.h",           "func": vd_vj_vk      },
   # { "name": "vslt.w",           "func": vd_vj_vk      },
   # { "name": "vslt.d",           "func": vd_vj_vk      },
   # { "name": "vslti.b",          "func": vd_vj_si5     },
   # { "name": "vslti.h",          "func": vd_vj_si5     },
   # { "name": "vslti.w",          "func": vd_vj_si5     },
   # { "name": "vslti.d",          "func": vd_vj_si5     },
   # { "name": "vslt.bu",          "func": vd_vj_vk      },
   # { "name": "vslt.hu",          "func": vd_vj_vk      },
   # { "name": "vslt.wu",          "func": vd_vj_vk      },
   # { "name": "vslt.du",          "func": vd_vj_vk      },
   # { "name": "vslti.bu",         "func": vd_vj_ui5     },
   # { "name": "vslti.hu",         "func": vd_vj_ui5     },
   # { "name": "vslti.wu",         "func": vd_vj_ui5     },
   # { "name": "vslti.du",         "func": vd_vj_ui5     },
   # { "name": "xvslt.b",          "func": xd_xj_xk      },
   # { "name": "xvslt.h",          "func": xd_xj_xk      },
   # { "name": "xvslt.w",          "func": xd_xj_xk      },
   # { "name": "xvslt.d",          "func": xd_xj_xk      },
   # { "name": "xvslti.b",         "func": xd_xj_si5     },
   # { "name": "xvslti.h",         "func": xd_xj_si5     },
   # { "name": "xvslti.w",         "func": xd_xj_si5     },
   # { "name": "xvslti.d",         "func": xd_xj_si5     },
   # { "name": "xvslt.bu",         "func": xd_xj_xk      },
   # { "name": "xvslt.hu",         "func": xd_xj_xk      },
   # { "name": "xvslt.wu",         "func": xd_xj_xk      },
   # { "name": "xvslt.du",         "func": xd_xj_xk      },
   # { "name": "xvslti.bu",        "func": xd_xj_ui5     },
   # { "name": "xvslti.hu",        "func": xd_xj_ui5     },
   # { "name": "xvslti.wu",        "func": xd_xj_ui5     },
   # { "name": "xvslti.du",        "func": xd_xj_ui5     },
   # { "name": "vbitsel.v",        "func": vd_vj_vk_va   },
   # { "name": "vbitseli.b",       "func": vd_vj_ui8     },
   # { "name": "xvbitsel.v",       "func": xd_xj_xk_xa   },
   # { "name": "xvbitseli.b",      "func": xd_xj_ui8     },
   # { "name": "vseteqz.v",        "func": cd_vj         },
   # { "name": "vsetnez.v",        "func": cd_vj         },
   # { "name": "vsetanyeqz.b",     "func": cd_vj         },
   # { "name": "vsetanyeqz.h",     "func": cd_vj         },
   # { "name": "vsetanyeqz.w",     "func": cd_vj         },
   # { "name": "vsetanyeqz.d",     "func": cd_vj         },
   # { "name": "vsetallnez.b",     "func": cd_vj         },
   # { "name": "vsetallnez.h",     "func": cd_vj         },
   # { "name": "vsetallnez.w",     "func": cd_vj         },
   # { "name": "vsetallnez.d",     "func": cd_vj         },
   # { "name": "xvseteqz.v",       "func": cd_xj         },
   # { "name": "xvsetnez.v",       "func": cd_xj         },
   # { "name": "xvsetanyeqz.b",    "func": cd_xj         },
   # { "name": "xvsetanyeqz.h",    "func": cd_xj         },
   # { "name": "xvsetanyeqz.w",    "func": cd_xj         },
   # { "name": "xvsetanyeqz.d",    "func": cd_xj         },
   # { "name": "xvsetallnez.b",    "func": cd_xj         },
   # { "name": "xvsetallnez.h",    "func": cd_xj         },
   # { "name": "xvsetallnez.w",    "func": cd_xj         },
   # { "name": "xvsetallnez.d",    "func": cd_xj         },

###########Vector moving and shuffling insns
   # { "name": "vinsgr2vr.b",      "func": vd_rj_ui4     },
   # { "name": "vinsgr2vr.h",      "func": vd_rj_ui3     },
   # { "name": "vinsgr2vr.w",      "func": vd_rj_ui2     },
   # { "name": "vinsgr2vr.d",      "func": vd_rj_ui1     },
   # { "name": "xvinsgr2vr.w",     "func": xd_rj_ui3     },
   # { "name": "xvinsgr2vr.d",     "func": xd_rj_ui2     },
   # { "name": "vpickve2gr.b",     "func": rd_vj_ui4     },
   # { "name": "vpickve2gr.h",     "func": rd_vj_ui3     },
   # { "name": "vpickve2gr.w",     "func": rd_vj_ui2     },
   # { "name": "vpickve2gr.d",     "func": rd_vj_ui1     },
   # { "name": "vpickve2gr.bu",    "func": rd_vj_ui4     },
   # { "name": "vpickve2gr.hu",    "func": rd_vj_ui3     },
   # { "name": "vpickve2gr.wu",    "func": rd_vj_ui2     },
   # { "name": "vpickve2gr.du",    "func": rd_vj_ui1     },
   # { "name": "xvpickve2gr.w",    "func": rd_xj_ui3     },
   # { "name": "xvpickve2gr.d",    "func": rd_xj_ui2     },
   # { "name": "xvpickve2gr.wu",   "func": rd_xj_ui3     },
   # { "name": "xvpickve2gr.du",   "func": rd_xj_ui2     },
   # { "name": "vreplgr2vr.b",     "func": vd_rj         },
   # { "name": "vreplgr2vr.h",     "func": vd_rj         },
   # { "name": "vreplgr2vr.w",     "func": vd_rj         },
   # { "name": "vreplgr2vr.d",     "func": vd_rj         },
   # { "name": "xvreplgr2vr.b",    "func": xd_rj         },
   # { "name": "xvreplgr2vr.h",    "func": xd_rj         },
   # { "name": "xvreplgr2vr.w",    "func": xd_rj         },
   # { "name": "xvreplgr2vr.d",    "func": xd_rj         },
   # { "name": "vreplve.b",        "func": vd_vj_rk      },
   # { "name": "vreplve.h",        "func": vd_vj_rk      },
   # { "name": "vreplve.w",        "func": vd_vj_rk      },
   # { "name": "vreplve.d",        "func": vd_vj_rk      },
   # { "name": "xvreplve.b",       "func": xd_xj_rk      },
   # { "name": "xvreplve.h",       "func": xd_xj_rk      },
   # { "name": "xvreplve.w",       "func": xd_xj_rk      },
   # { "name": "xvreplve.d",       "func": xd_xj_rk      },
   # { "name": "vreplvei.b",       "func": vd_vj_ui4     },
   # { "name": "vreplvei.h",       "func": vd_vj_ui3     },
   # { "name": "vreplvei.w",       "func": vd_vj_ui2     },
   # { "name": "vreplvei.d",       "func": vd_vj_ui1     },
   # { "name": "xvrepl128vei.b",   "func": xd_xj_ui4     },
   # { "name": "xvrepl128vei.h",   "func": xd_xj_ui3     },
   # { "name": "xvrepl128vei.w",   "func": xd_xj_ui2     },
   # { "name": "xvrepl128vei.d",   "func": xd_xj_ui1     },
   # { "name": "xvreplve0.b",      "func": xd_xj         },
   # { "name": "xvreplve0.h",      "func": xd_xj         },
   # { "name": "xvreplve0.w",      "func": xd_xj         },
   # { "name": "xvreplve0.d",      "func": xd_xj         },
   # { "name": "xvreplve0.q",      "func": xd_xj         },
   # { "name": "xvinsve0.w",       "func": xd_xj_ui3     },
   # { "name": "xvinsve0.d",       "func": xd_xj_ui2     },
   # { "name": "vpackev.b",        "func": vd_vj_vk      },
   # { "name": "vpackev.h",        "func": vd_vj_vk      },
   # { "name": "vpackev.w",        "func": vd_vj_vk      },
   # { "name": "vpackev.d",        "func": vd_vj_vk      },
   # { "name": "vpackod.b",        "func": vd_vj_vk      },
   # { "name": "vpackod.h",        "func": vd_vj_vk      },
   # { "name": "vpackod.w",        "func": vd_vj_vk      },
   # { "name": "vpackod.d",        "func": vd_vj_vk      },
   # { "name": "vpickev.b",        "func": vd_vj_vk      },
   # { "name": "vpickev.h",        "func": vd_vj_vk      },
   # { "name": "vpickev.w",        "func": vd_vj_vk      },
   # { "name": "vpickev.d",        "func": vd_vj_vk      },
   # { "name": "vpickod.b",        "func": vd_vj_vk      },
   # { "name": "vpickod.h",        "func": vd_vj_vk      },
   # { "name": "vpickod.w",        "func": vd_vj_vk      },
   # { "name": "vpickod.d",        "func": vd_vj_vk      },
   # { "name": "vilvh.b",          "func": vd_vj_vk      },
   # { "name": "vilvh.h",          "func": vd_vj_vk      },
   # { "name": "vilvh.w",          "func": vd_vj_vk      },
   # { "name": "vilvh.d",          "func": vd_vj_vk      },
   # { "name": "vilvl.b",          "func": vd_vj_vk      },
   # { "name": "vilvl.h",          "func": vd_vj_vk      },
   # { "name": "vilvl.w",          "func": vd_vj_vk      },
   # { "name": "vilvl.d",          "func": vd_vj_vk      },
   # { "name": "xvpackev.b",       "func": xd_xj_xk      },
   # { "name": "xvpackev.h",       "func": xd_xj_xk      },
   # { "name": "xvpackev.w",       "func": xd_xj_xk      },
   # { "name": "xvpackev.d",       "func": xd_xj_xk      },
   # { "name": "xvpackod.b",       "func": xd_xj_xk      },
   # { "name": "xvpackod.h",       "func": xd_xj_xk      },
   # { "name": "xvpackod.w",       "func": xd_xj_xk      },
   # { "name": "xvpackod.d",       "func": xd_xj_xk      },
   # { "name": "xvpickev.b",       "func": xd_xj_xk      },
   # { "name": "xvpickev.h",       "func": xd_xj_xk      },
   # { "name": "xvpickev.w",       "func": xd_xj_xk      },
   # { "name": "xvpickev.d",       "func": xd_xj_xk      },
   # { "name": "xvpickod.b",       "func": xd_xj_xk      },
   # { "name": "xvpickod.h",       "func": xd_xj_xk      },
   # { "name": "xvpickod.w",       "func": xd_xj_xk      },
   # { "name": "xvpickod.d",       "func": xd_xj_xk      },
   # { "name": "xvilvh.b",         "func": xd_xj_xk      },
   # { "name": "xvilvh.h",         "func": xd_xj_xk      },
   # { "name": "xvilvh.w",         "func": xd_xj_xk      },
   # { "name": "xvilvh.d",         "func": xd_xj_xk      },
   # { "name": "xvilvl.b",         "func": xd_xj_xk      },
   # { "name": "xvilvl.h",         "func": xd_xj_xk      },
   # { "name": "xvilvl.w",         "func": xd_xj_xk      },
   # { "name": "xvilvl.d",         "func": xd_xj_xk      },
   # { "name": "vshuf.b",          "func": vd_vj_vk_va   },
   # { "name": "vshuf.h",          "func": vd_vj_vk      },
   # { "name": "vshuf.w",          "func": vd_vj_vk      },
   # { "name": "vshuf.d",          "func": vd_vj_vk      },
   # { "name": "xvshuf.b",         "func": xd_xj_xk_xa   },
   # { "name": "xvshuf.h",         "func": xd_xj_xk      },
   # { "name": "xvshuf.w",         "func": xd_xj_xk      },
   # { "name": "xvshuf.d",         "func": xd_xj_xk      },
   # { "name": "xvperm.w",         "func": xd_xj_xk      },
   # { "name": "vshuf4i.b",        "func": vd_vj_ui8     },
   # { "name": "vshuf4i.h",        "func": vd_vj_ui8     },
   # { "name": "vshuf4i.w",        "func": vd_vj_ui8     },
   # { "name": "vshuf4i.d",        "func": vd_vj_ui8     },
   # { "name": "xvshuf4i.b",       "func": xd_xj_ui8     },
   # { "name": "xvshuf4i.h",       "func": xd_xj_ui8     },
   # { "name": "xvshuf4i.w",       "func": xd_xj_ui8     },
   # { "name": "xvshuf4i.d",       "func": xd_xj_ui8     },
   # { "name": "vpermi.w",         "func": vd_vj_ui8     },
   # { "name": "xvpermi.w",        "func": xd_xj_ui8     },
   # { "name": "xvpermi.d",        "func": xd_xj_ui8     },
   # { "name": "xvpermi.q",        "func": xd_xj_ui8     },
   # { "name": "vextrins.b",       "func": vd_vj_ui8     },
   # { "name": "vextrins.h",       "func": vd_vj_ui8     },
   # { "name": "vextrins.w",       "func": vd_vj_ui8     },
   # { "name": "vextrins.d",       "func": vd_vj_ui8     },
   # { "name": "xvextrins.b",      "func": xd_xj_ui8     },
   # { "name": "xvextrins.h",      "func": xd_xj_ui8     },
   # { "name": "xvextrins.w",      "func": xd_xj_ui8     },
   # { "name": "xvextrins.d",      "func": xd_xj_ui8     },

###########Vector load/store insns
   # { "name": "vld",              "func": vd_vj_si12    },
   # { "name": "xvld",             "func": xd_xj_si12    },
   # { "name": "vst",              "func": vd_vj_si12    },
   # { "name": "xvst",             "func": xd_xj_si12    },
   # { "name": "vldx",             "func": vd_vj_rk      },
   # { "name": "xvldx",            "func": xd_xj_rk      },
   # { "name": "vstx",             "func": vd_vj_rk      },
   # { "name": "xvstx",            "func": xd_xj_rk      },
   # { "name": "vldrepl.b",        "func": _vd_rj_si12   },
   # { "name": "vldrepl.h",        "func": _vd_rj_si11   },
   # { "name": "vldrepl.w",        "func": _vd_rj_si10   },
   # { "name": "vldrepl.d",        "func": _vd_rj_si9    },
   # { "name": "vstelm.b",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.h",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.w",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.d",         "func": vd_rj_si8_idx },

###########Least insns
   # { "name": "xvmin.bu",          "func": xd_xj_xk     },
   # { "name": "xvreplgr2vr.b",     "func": xd_rj        },
   # { "name": "xvmax.bu",          "func": xd_xj_xk     },
   # { "name": "xvseq.b",           "func": xd_xj_xk     },
   # { "name": "xvxor.v",           "func": xd_xj_xk     },
   # { "name": "xvsetanyeqz.b",     "func": cd_xj        },
   # { "name": "xvseteqz.v",        "func": cd_xj        },
   # { "name": "xvpickve.w",        "func": xd_xj_ui3    },
   # { "name": "xvpermi.q",         "func": xd_xj_ui3    },
   # { "name": "xvmsknz.b",         "func": xd_xj        },
   # { "name": "vadd.b",           "func": vd_vj_vk      },
   # { "name": "vadd.b",           "func": vd_vj_vk      },
   # { "name": "vsub.b",           "func": vd_vj_vk      },
   # { "name": "vaddi.bu",         "func": vd_vj_ui5     },
   # { "name": "vmax.bu",          "func": vd_vj_vk      },
   # { "name": "vmin.bu",          "func": vd_vj_vk      },
   # { "name": "vmsknz.b",         "func": vd_vj         },
   # { "name": "vand.v",           "func": vd_vj_vk      },
   # { "name": "vor.v",            "func": vd_vj_vk      },
   # { "name": "vxor.v",           "func": vd_vj_vk      },
   # { "name": "vorn.v",           "func": vd_vj_vk      },
   # { "name": "vnori.b",          "func": vd_vj_ui8     },
   # { "name": "vfrstpi.b",        "func": vd_vj_ui5     },
   # { "name": "vseq.b",           "func": vd_vj_vk      },
   # { "name": "vseqi.b",          "func": vd_vj_si5     },
   # { "name": "vslt.b",           "func": vd_vj_vk      },
   # { "name": "vseteqz.v",        "func": cd_vj         },
   # { "name": "vsetanyeqz.b",     "func": cd_vj         },
   # { "name": "vpickve2gr.bu",    "func": rd_vj_ui4     },
   # { "name": "vreplgr2vr.b",     "func": vd_rj         },
   # { "name": "vreplve.b",        "func": vd_vj_rk      },
   # { "name": "vilvl.h",          "func": vd_vj_vk      },
   # { "name": "vilvl.w",          "func": vd_vj_vk      },
   # { "name": "vshuf.b",          "func": vd_vj_vk_va   },
   # { "name": "vldrepl.h",        "func": vd_rj_si11    },
   # { "name": "vldrepl.d",        "func": vd_rj_si9     },
   # { "name": "vstelm.b",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.h",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.w",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.d",         "func": vd_rj_si8_idx },
]

#n = 28
n = 10
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
