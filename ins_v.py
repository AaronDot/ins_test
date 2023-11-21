import os

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
    for _ in range(0, n):
        line = func(name, n)
        if build(line) != 0:
            print("Build failed!")
            return False
        if not diff():
            return False
    return True

def vd_vj_vk(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, 0x70\n    "
    line += f"vld $vr2, $t0, 0x80\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj_vk1(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"vld $vr2, $t0, {0x8 * (n+1)}\n    "
#    line += f"vld $vr1, $t0, 0x40\n    "
#    line += f"vld $vr2, $t0, 0x30\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line


def vd_vj(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $vr1\n"
    return line

def vd_rj(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"ld.d $r1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $r1\n"
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
    line += f"{name} $vr0, $vr1, $vr2, $vr3\n"
    return line

def vd_rj_ui(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"ld.d $t1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $t1, 1\n"
    return line

def rd_vj_ui(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr0, $t0, {0x8 * n}\n    "
    line += f"{name} $r12, $vr0, 1\n"
    return line

def vd_vj_ui(name, n):
    line =  "la.local $t0, mem_j\n    "
    line += f"vld $vr1, $t0, {0x8 * n}\n    "
    line += f"{name} $vr0, $vr1, 7\n"
    return line

insts = [
   # { "name": "vseq.b",         "func": vd_vj_vk },
   # { "name": "vand.v",         "func": vd_vj_vk },
   # { "name": "vmsknz.b",      "func": vd_vj },
   # { "name": "vilvl.h",      "func": vd_vj_vk },
   # { "name": "vldi",         "func": vd_si },
   # { "name": "vmskgez.b",      "func": vd_vj },
   # { "name": "vshuf.b",         "func": vd_vj_vk_va },
   # { "name": "vpickve2gr.b",   "func": rd_vj_ui },
   # { "name": "vaddi.bu",       "func": vd_vj_ui },

    { "name": "vneg.b",           "func": vd_vj },
    { "name": "vneg.h",           "func": vd_vj },
    { "name": "vneg.w",           "func": vd_vj },
    { "name": "vneg.d",           "func": vd_vj },
    { "name": "vadd.b",           "func": vd_vj_vk1 },
    { "name": "vadd.h",           "func": vd_vj_vk1 },
    { "name": "vadd.w",           "func": vd_vj_vk1 },
    { "name": "vadd.d",           "func": vd_vj_vk1 },
    { "name": "vsub.b",           "func": vd_vj_vk1 },
    { "name": "vsub.h",           "func": vd_vj_vk1 },
    { "name": "vsub.w",           "func": vd_vj_vk1 },
    { "name": "vsub.d",           "func": vd_vj_vk1 },
    { "name": "vhaddw.h.b",       "func": vd_vj_vk1 },
    { "name": "vhaddw.w.h",       "func": vd_vj_vk1 },
    { "name": "vhaddw.d.w",       "func": vd_vj_vk1 },
    { "name": "vhaddw.q.d",       "func": vd_vj_vk1 },
    { "name": "vhsubw.h.b",       "func": vd_vj_vk1 },
    { "name": "vhsubw.w.h",       "func": vd_vj_vk1 },
    { "name": "vhsubw.d.w",       "func": vd_vj_vk1 },
    { "name": "vhsubw.q.d",       "func": vd_vj_vk1 },
    { "name": "vhaddw.hu.bu",     "func": vd_vj_vk1 },
    { "name": "vhaddw.wu.hu",     "func": vd_vj_vk1 },
    { "name": "vhaddw.du.wu",     "func": vd_vj_vk1 },
    { "name": "vhaddw.qu.du",     "func": vd_vj_vk1 },
    { "name": "vhsubw.hu.bu",     "func": vd_vj_vk1 },
    { "name": "vhsubw.wu.hu",     "func": vd_vj_vk1 },
    { "name": "vhsubw.du.wu",     "func": vd_vj_vk1 },
    { "name": "vhsubw.qu.du",     "func": vd_vj_vk1 },
    { "name": "vaddwev.h.b",      "func": vd_vj_vk1 },
    { "name": "vaddwev.w.h",      "func": vd_vj_vk1 },
    { "name": "vaddwev.d.w",      "func": vd_vj_vk1 },
    { "name": "vaddwev.q.d",      "func": vd_vj_vk1 },
    { "name": "vsubwev.h.b",      "func": vd_vj_vk1 },
    { "name": "vsubwev.w.h",      "func": vd_vj_vk1 },
    { "name": "vsubwev.d.w",      "func": vd_vj_vk1 },
    { "name": "vsubwev.q.d",      "func": vd_vj_vk1 },
    { "name": "vaddwod.h.b",      "func": vd_vj_vk1 },
    { "name": "vaddwod.w.h",      "func": vd_vj_vk1 },
    { "name": "vaddwod.d.w",      "func": vd_vj_vk1 },
    { "name": "vaddwod.q.d",      "func": vd_vj_vk1 },
    { "name": "vsubwod.h.b",      "func": vd_vj_vk1 },
    { "name": "vsubwod.w.h",      "func": vd_vj_vk1 },
    { "name": "vsubwod.d.w",      "func": vd_vj_vk1 },
    { "name": "vsubwod.q.d",      "func": vd_vj_vk1 },
    { "name": "vaddwev.h.bu",     "func": vd_vj_vk1 },
    { "name": "vaddwev.w.hu",     "func": vd_vj_vk1 },
    { "name": "vaddwev.d.wu",     "func": vd_vj_vk1 },
    { "name": "vaddwev.q.du",     "func": vd_vj_vk1 },
    { "name": "vsubwev.h.bu",     "func": vd_vj_vk1 },
    { "name": "vsubwev.w.hu",     "func": vd_vj_vk1 },
    { "name": "vsubwev.d.wu",     "func": vd_vj_vk1 },
    { "name": "vsubwev.q.du",     "func": vd_vj_vk1 },
    { "name": "vaddwod.h.bu",     "func": vd_vj_vk1 },
    { "name": "vaddwod.w.hu",     "func": vd_vj_vk1 },
    { "name": "vaddwod.d.wu",     "func": vd_vj_vk1 },
    { "name": "vaddwod.q.du",     "func": vd_vj_vk1 },
    { "name": "vsubwod.h.bu",     "func": vd_vj_vk1 },
    { "name": "vsubwod.w.hu",     "func": vd_vj_vk1 },
    { "name": "vsubwod.d.wu",     "func": vd_vj_vk1 },
    { "name": "vsubwod.q.du",     "func": vd_vj_vk1 },
    { "name": "vaddwev.h.bu.b",   "func": vd_vj_vk1 },
    { "name": "vaddwev.w.hu.h",   "func": vd_vj_vk1 },
    { "name": "vaddwev.d.wu.w",   "func": vd_vj_vk1 },
    { "name": "vaddwev.q.du.d",   "func": vd_vj_vk1 },
    { "name": "vaddwod.h.bu.b",   "func": vd_vj_vk1 },
    { "name": "vaddwod.w.hu.h",   "func": vd_vj_vk1 },
    { "name": "vaddwod.d.wu.w",   "func": vd_vj_vk1 },
    { "name": "vaddwod.q.du.d",   "func": vd_vj_vk1 },
    { "name": "vavgr.b",          "func": vd_vj_vk1 },
    { "name": "vavgr.h",          "func": vd_vj_vk1 },
    { "name": "vavgr.w",          "func": vd_vj_vk1 },
    { "name": "vavgr.d",          "func": vd_vj_vk1 },
    { "name": "vsadd.b",          "func": vd_vj_vk1 },
    { "name": "vsadd.h",          "func": vd_vj_vk1 },
    { "name": "vsadd.w",          "func": vd_vj_vk1 },
    { "name": "vsadd.d",          "func": vd_vj_vk1 },
    { "name": "vssub.b",          "func": vd_vj_vk1 },
    { "name": "vssub.h",          "func": vd_vj_vk1 },
    { "name": "vssub.w",          "func": vd_vj_vk1 },
    { "name": "vssub.d",          "func": vd_vj_vk1 },
    { "name": "vsadd.bu",         "func": vd_vj_vk1 },
    { "name": "vsadd.hu",         "func": vd_vj_vk1 },
    { "name": "vsadd.wu",         "func": vd_vj_vk1 },
    { "name": "vsadd.du",         "func": vd_vj_vk1 },
    { "name": "vssub.bu",         "func": vd_vj_vk1 },
    { "name": "vssub.hu",         "func": vd_vj_vk1 },
    { "name": "vssub.wu",         "func": vd_vj_vk1 },
    { "name": "vssub.du",         "func": vd_vj_vk1 },
    { "name": "vexth.h.b",        "func": vd_vj },
    { "name": "vexth.w.h",        "func": vd_vj },
    { "name": "vexth.d.w",        "func": vd_vj },
    { "name": "vexth.q.d",        "func": vd_vj },
    { "name": "vexth.hu.bu",      "func": vd_vj },
    { "name": "vexth.wu.hu",      "func": vd_vj },
    { "name": "vexth.du.wu",      "func": vd_vj },
    { "name": "vexth.qu.du",      "func": vd_vj },
    { "name": "vand.v",           "func": vd_vj_vk1 },
    { "name": "vor.v",            "func": vd_vj_vk1 },
    { "name": "vxor.v",           "func": vd_vj_vk1 },
    { "name": "vnor.v",           "func": vd_vj_vk1 },
    { "name": "vandn.v",          "func": vd_vj_vk1 },
    { "name": "vorn.v",           "func": vd_vj_vk1 },
    { "name": "vandi.b",          "func": vd_vj_ui },
    { "name": "vori.b",           "func": vd_vj_ui },
    { "name": "vxori.b",          "func": vd_vj_ui },
    { "name": "vnori.b",          "func": vd_vj_ui },
    { "name": "vseq.b",           "func": vd_vj_vk1 },
    { "name": "vseq.h",           "func": vd_vj_vk1 },
    { "name": "vseq.w",           "func": vd_vj_vk1 },
    { "name": "vseq.d",           "func": vd_vj_vk1 },
    { "name": "vilvh.b",          "func": vd_vj_vk1 },
    { "name": "vilvh.h",          "func": vd_vj_vk1 },
    { "name": "vilvh.w",          "func": vd_vj_vk1 },
    { "name": "vilvh.d",          "func": vd_vj_vk1 },
    { "name": "vilvl.b",          "func": vd_vj_vk1 },
    { "name": "vilvl.h",          "func": vd_vj_vk1 },
    { "name": "vilvl.w",          "func": vd_vj_vk1 },
    { "name": "vilvl.d",          "func": vd_vj_vk1 },
    { "name": "vadd.q",           "func": vd_vj_vk1 },
    { "name": "vsub.q",           "func": vd_vj_vk1 },
    { "name": "vadda.b",          "func": vd_vj_vk1 },
    { "name": "vadda.h",          "func": vd_vj_vk1 },
    { "name": "vadda.w",          "func": vd_vj_vk1 },
    { "name": "vadda.d",          "func": vd_vj_vk1 },
    { "name": "vmax.b",           "func": vd_vj_vk1 },
    { "name": "vmax.h",           "func": vd_vj_vk1 },
    { "name": "vmax.w",           "func": vd_vj_vk1 },
    { "name": "vmax.d",           "func": vd_vj_vk1 },
    { "name": "vmax.bu",          "func": vd_vj_vk1 },
    { "name": "vmax.hu",          "func": vd_vj_vk1 },
    { "name": "vmax.wu",          "func": vd_vj_vk1 },
    { "name": "vmax.du",          "func": vd_vj_vk1 },
    { "name": "vmin.b",           "func": vd_vj_vk1 },
    { "name": "vmin.h",           "func": vd_vj_vk1 },
    { "name": "vmin.w",           "func": vd_vj_vk1 },
    { "name": "vmin.d",           "func": vd_vj_vk1 },
    { "name": "vmin.bu",          "func": vd_vj_vk1 },
    { "name": "vmin.hu",          "func": vd_vj_vk1 },
    { "name": "vmin.wu",          "func": vd_vj_vk1 },
    { "name": "vmin.du",          "func": vd_vj_vk1 },
    { "name": "vmaxi.b",          "func": vd_vj_ui },
    { "name": "vmaxi.h",          "func": vd_vj_ui },
    { "name": "vmaxi.w",          "func": vd_vj_ui },
    { "name": "vmaxi.d",          "func": vd_vj_ui },
    { "name": "vmini.b",          "func": vd_vj_ui },
    { "name": "vmini.h",          "func": vd_vj_ui },
    { "name": "vmini.w",          "func": vd_vj_ui },
    { "name": "vmini.d",          "func": vd_vj_ui },
    { "name": "vmaxi.bu",         "func": vd_vj_ui },
    { "name": "vmaxi.hu",         "func": vd_vj_ui },
    { "name": "vmaxi.wu",         "func": vd_vj_ui },
    { "name": "vmaxi.du",         "func": vd_vj_ui },
    { "name": "vmini.bu",         "func": vd_vj_ui },
    { "name": "vmini.hu",         "func": vd_vj_ui },
    { "name": "vmini.wu",         "func": vd_vj_ui },
    { "name": "vmini.du",         "func": vd_vj_ui },
    { "name": "vmul.b",           "func": vd_vj_vk1 },
    { "name": "vmul.h",           "func": vd_vj_vk1 },
    { "name": "vmul.w",           "func": vd_vj_vk1 },
    { "name": "vmul.d",           "func": vd_vj_vk1 },
    { "name": "vmuh.b",           "func": vd_vj_vk1 },
    { "name": "vmuh.h",           "func": vd_vj_vk1 },
    { "name": "vmuh.w",           "func": vd_vj_vk1 },
    { "name": "vmuh.d",           "func": vd_vj_vk1 },
    { "name": "vmuh.bu",          "func": vd_vj_vk1 },
    { "name": "vmuh.hu",          "func": vd_vj_vk1 },
    { "name": "vmuh.wu",          "func": vd_vj_vk1 },
    { "name": "vmuh.du",          "func": vd_vj_vk1 },
    { "name": "vmadd.b",          "func": vd_vj_vk1 },
    { "name": "vmadd.h",          "func": vd_vj_vk1 },
    { "name": "vmadd.w",          "func": vd_vj_vk1 },
    { "name": "vmadd.d",          "func": vd_vj_vk1 },
    { "name": "vmsub.b",          "func": vd_vj_vk1 },
    { "name": "vmsub.h",          "func": vd_vj_vk1 },
    { "name": "vmsub.w",          "func": vd_vj_vk1 },
    { "name": "vmsub.d",          "func": vd_vj_vk1 },
    { "name": "vmulwev.h.b",      "func": vd_vj_vk1 },
    { "name": "vmulwev.w.h",      "func": vd_vj_vk1 },
    { "name": "vmulwev.d.w",      "func": vd_vj_vk1 },
    { "name": "vmulwev.q.d",      "func": vd_vj_vk1 },
    { "name": "vmulwod.h.b",      "func": vd_vj_vk1 },
    { "name": "vmulwod.w.h",      "func": vd_vj_vk1 },
    { "name": "vmulwod.d.w",      "func": vd_vj_vk1 },
    { "name": "vmulwod.q.d",      "func": vd_vj_vk1 },
    { "name": "vmulwev.h.bu",     "func": vd_vj_vk1 },
    { "name": "vmulwev.w.hu",     "func": vd_vj_vk1 },
    { "name": "vmulwev.d.wu",     "func": vd_vj_vk1 },
    { "name": "vmulwev.q.du",     "func": vd_vj_vk1 },
    { "name": "vmulwod.h.bu",     "func": vd_vj_vk1 },
    { "name": "vmulwod.w.hu",     "func": vd_vj_vk1 },
    { "name": "vmulwod.d.wu",     "func": vd_vj_vk1 },
    { "name": "vmulwod.q.du",     "func": vd_vj_vk1 },
    { "name": "vseteqz.v",        "func": cd_vj },
    { "name": "vsetanyeqz.b",     "func": cd_vj },
    { "name": "vsetanyeqz.h",     "func": cd_vj },
    { "name": "vsetanyeqz.w",     "func": cd_vj },
    { "name": "vsetanyeqz.d",     "func": cd_vj },
    { "name": "vinsgr2vr.b",      "func": vd_rj_ui },
    { "name": "vinsgr2vr.h",      "func": vd_rj_ui },
    { "name": "vinsgr2vr.w",      "func": vd_rj_ui },
    { "name": "vinsgr2vr.d",      "func": vd_rj_ui },
    { "name": "vsll.b",           "func": vd_vj_vk1 },
    { "name": "vsll.h",           "func": vd_vj_vk1 },
    { "name": "vsll.w",           "func": vd_vj_vk1 },
    { "name": "vsll.d",           "func": vd_vj_vk1 },
    { "name": "vsrl.b",           "func": vd_vj_vk1 },
    { "name": "vsrl.h",           "func": vd_vj_vk1 },
    { "name": "vsrl.w",           "func": vd_vj_vk1 },
    { "name": "vsrl.d",           "func": vd_vj_vk1 },
    { "name": "vsra.b",           "func": vd_vj_vk1 },
    { "name": "vsra.h",           "func": vd_vj_vk1 },
    { "name": "vsra.w",           "func": vd_vj_vk1 },
    { "name": "vsra.d",           "func": vd_vj_vk1 },
    { "name": "vslli.b",          "func": vd_vj_ui },
    { "name": "vslli.h",          "func": vd_vj_ui },
    { "name": "vslli.w",          "func": vd_vj_ui },
    { "name": "vslli.d",          "func": vd_vj_ui },
    { "name": "vsrli.b",          "func": vd_vj_ui },
    { "name": "vsrli.h",          "func": vd_vj_ui },
    { "name": "vsrli.w",          "func": vd_vj_ui },
    { "name": "vsrli.d",          "func": vd_vj_ui },
    { "name": "vsrai.b",          "func": vd_vj_ui },
    { "name": "vsrai.h",          "func": vd_vj_ui },
    { "name": "vsrai.w",          "func": vd_vj_ui },
    { "name": "vsrai.d",          "func": vd_vj_ui },
    { "name": "vsllwil.h.b",      "func": vd_vj_ui },
    { "name": "vsllwil.w.h",      "func": vd_vj_ui },
    { "name": "vsllwil.d.w",      "func": vd_vj_ui },
    { "name": "vextl.q.d",        "func": vd_vj },
    { "name": "vsllwil.hu.bu",    "func": vd_vj_ui },
    { "name": "vsllwil.wu.hu",    "func": vd_vj_ui },
    { "name": "vsllwil.du.wu",    "func": vd_vj_ui },
    { "name": "vextl.qu.du",      "func": vd_vj },
    { "name": "vaddi.bu",         "func": vd_vj_ui },
    { "name": "vaddi.hu",         "func": vd_vj_ui },
    { "name": "vaddi.wu",         "func": vd_vj_ui },
    { "name": "vaddi.du",         "func": vd_vj_ui },
    { "name": "vreplgr2vr.b",     "func": vd_rj },
    { "name": "vreplgr2vr.h",     "func": vd_rj },
    { "name": "vreplgr2vr.w",     "func": vd_rj },
    { "name": "vreplgr2vr.d",     "func": vd_rj },
    { "name": "vmaddwev.h.b",     "func": vd_vj_vk1 },
    { "name": "vmaddwev.w.h",     "func": vd_vj_vk1 },
    { "name": "vmaddwev.d.w",     "func": vd_vj_vk1 },
    { "name": "vmaddwev.q.d",     "func": vd_vj_vk1 },
    { "name": "vmaddwod.h.b",     "func": vd_vj_vk1 },
    { "name": "vmaddwod.w.h",     "func": vd_vj_vk1 },
    { "name": "vmaddwod.d.w",     "func": vd_vj_vk1 },
    { "name": "vmaddwod.q.d",     "func": vd_vj_vk1 },
    { "name": "vmaddwev.h.bu",    "func": vd_vj_vk1 },
    { "name": "vmaddwev.w.hu",    "func": vd_vj_vk1 },
    { "name": "vmaddwev.d.wu",    "func": vd_vj_vk1 },
    { "name": "vmaddwev.q.du",    "func": vd_vj_vk1 },
    { "name": "vmaddwod.h.bu",    "func": vd_vj_vk1 },
    { "name": "vmaddwod.w.hu",    "func": vd_vj_vk1 },
    { "name": "vmaddwod.d.wu",    "func": vd_vj_vk1 },
    { "name": "vmaddwod.q.du",    "func": vd_vj_vk1 },
]

n = 29
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
