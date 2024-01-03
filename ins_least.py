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

def xd_xj_xk(name, n):
    line =  "la.local $t0, mem_k\n    "
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
    line += f"vld $vr0, $t0, 0\n    "
    line += f"{name} $fcc1, $vr0\n"
    return line

def cd_xj(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr0, $t0, 0\n    "
    line += f"{name} $fcc1, $xr0\n"
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
    line += f"vld $vr0, $t0, {0x8 * 6}\n    "
    line += f"vld $vr1, $t0, {0x8 * (6 + 1)}\n    "
    #ui5 = rand_imm(5, False)
    ui5 = 0
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

def xd_xj_ui3(name, n):
    line =  "la.local $t0, mem_k\n    "
    line += f"xvld $xr1, $t0, {0x8 * n}\n    "
    ui3 = rand_imm(3, False)
    line += f"{name} $xr0, $xr1, {ui3}\n"
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

def vd_vj_vk_s(name, n):
    line =  "la.local $t0, dataf\n    "
    line += f"vld $vr1, $t0, {0x8 * 2}\n    "
    line += f"vld $vr2, $t0, {0x8 * 3}\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

insts = [
   # { "name": "xvmin.bu",          "func": xd_xj_xk  },
   # { "name": "xvreplgr2vr.b",     "func": xd_rj       },
   # { "name": "xvmax.bu",          "func": xd_xj_xk  },
   # { "name": "xvseq.b",           "func": xd_xj_xk  },
   # { "name": "xvxor.v",           "func": xd_xj_xk  },
   # { "name": "xvsetanyeqz.b",     "func": cd_xj       },
   # { "name": "xvseteqz.v",        "func": cd_xj       },
   # { "name": "xvpickve.w",        "func": xd_xj_ui3       },
   # { "name": "xvpermi.q",         "func": xd_xj_ui3       },
   # { "name": "xvmsknz.b",         "func": xd_xj     },

   # { "name": "vadd.b",           "func": vd_vj_vk  },
   # { "name": "vadd.b",           "func": vd_vj_vk  },
   # { "name": "vsub.b",           "func": vd_vj_vk  },
   # { "name": "vaddi.bu",         "func": vd_vj_ui5 },
   # { "name": "vmax.bu",          "func": vd_vj_vk  },
   # { "name": "vmin.bu",          "func": vd_vj_vk  },
   # { "name": "vmsknz.b",         "func": vd_vj     },
   # { "name": "vand.v",           "func": vd_vj_vk  },
   # { "name": "vor.v",            "func": vd_vj_vk  },
   # { "name": "vxor.v",           "func": vd_vj_vk  },
   # { "name": "vorn.v",           "func": vd_vj_vk  },
   # { "name": "vnori.b",          "func": vd_vj_ui8 },
   # { "name": "vfrstpi.b",        "func": vd_vj_ui5 },
   # { "name": "vseq.b",           "func": vd_vj_vk    },
   # { "name": "vseqi.b",          "func": vd_vj_si5   },
   # { "name": "vslt.b",           "func": vd_vj_vk    },
   # { "name": "vseteqz.v",        "func": cd_vj       },
   # { "name": "vsetanyeqz.b",     "func": cd_vj       },
   # { "name": "vpickve2gr.bu",    "func": rd_vj_ui4   },
   # { "name": "vreplgr2vr.b",     "func": vd_rj       },
   # { "name": "vreplve.b",        "func": vd_vj_rk    },
   # { "name": "vilvl.h",          "func": vd_vj_vk    },
   # { "name": "vilvl.w",          "func": vd_vj_vk    },
   # { "name": "vshuf.b",          "func": vd_vj_vk_va },
   # { "name": "vldrepl.h",        "func": vd_rj_si11    },
   # { "name": "vldrepl.d",        "func": vd_rj_si9     },
    { "name": "vstelm.b",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.h",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.w",         "func": vd_rj_si8_idx },
   # { "name": "vstelm.d",         "func": vd_rj_si8_idx },
]

n = 28
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
