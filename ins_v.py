import os

def write(line, file):
    with open("dump.S", "r") as input:
        text = input.read()
        with open(file, "w") as output:
            output.write(text.replace("nop\n", line))

def build(line):
    write(line, "tmp.S")
    ret = os.system("gcc -nostdlib -static tmp.S show.c data_v.c -o tmp")
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
    line += "la.local $t1, mem_k\n    "
#    line += f"vld $vr1, $t0, {0x10 * n}\n    "
#    line += f"vld $vr2, $t1, {0x10 * n}\n    "
    line += f"vld $vr1, $t0, 0x40\n    "
    line += f"vld $vr2, $t1, 0x30\n    "
    line += f"{name} $vr0, $vr1, $vr2\n"
    return line

def vd_vj(name, n):
    line =  "la.local $t0, mem_j\n    "
#    line += f"vld $vr1, $t0, {0x10 * n}\n    "
#    line += f"vld $vr2, $t1, {0x10 * n}\n    "
    line += f"vld $vr1, $t0, 0x50\n    "
    line += f"{name} $vr0, $vr1\n"
    return line

def vd_rj(name, n):
    line =  "la.local $t0, mem_j\n    "
#    line += f"vld $vr1, $t0, {0x10 * n}\n    "
#    line += f"vld $vr2, $t1, {0x10 * n}\n    "
    line += f"ld.d $r1, $t0, 0x50\n    "
    line += f"{name} $vr0, $r1\n"
    return line

def cd_vj(name, n):
    line =  "la.local $t0, mem_j\n    "
#    line += f"vld $vr1, $t0, {0x10 * n}\n    "
#    line += f"vld $vr2, $t1, {0x10 * n}\n    "
    line += f"vld $vr1, $t0, 0x10\n    "
    line += f"{name} $fcc0, $vr1\n"
    return line

insts = [
    { "name": "vadd.b",         "func": vd_vj_vk },
    { "name": "vmskgez.b",      "func": vd_vj },
    { "name": "vseq.b",         "func": vd_vj_vk },
    { "name": "vand.v",         "func": vd_vj_vk },
    { "name": "vmsknz.b",      "func": vd_vj },
    { "name": "vilvl.h",      "func": vd_vj_vk },
    { "name": "vreplgr2vr.b",      "func": vd_rj },
    { "name": "vmax.bu",         "func": vd_vj_vk },
    { "name": "vseteqz.v",         "func": cd_vj }
]

n = 1
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
