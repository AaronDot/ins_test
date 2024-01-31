import os

def write(line, file):
    with open("dump_f.S", "r") as input:
        text = input.read()
        with open(file, "w") as output:
            output.write(text.replace("nop\n", line))


def build(line):
    write(line, "tmp.S")
    ret = os.system("gcc -nostdlib -static tmp.S show_f.c data.c -o tmp")
    if ret != 0:
        return ret
    ret = os.system("./tmp > want.txt 2>&1")
    if ret != 0:
        return ret
    #return os.system("/usr/local/bin/valgrind --tool=none -q ./tmp > out.txt 2>&1")
    return os.system("../valgrind --tool=none -q ./tmp > out.txt 2>&1")


def diff(high):
    with open("want.txt", "r") as want:
        with open("out.txt", "r") as out:
            lines1 = want.readlines()
            lines2 = out.readlines()
            if len(lines1) != len(lines2):
                print("len1 != len2")
                return False
            for i in range(0, len(lines1)):
                if high and lines1[i] != lines2[i]:
                    print("64-bit")
                    print("want: " + lines1[i] + "out: " + lines2[i])
                    return False
                elif lines1[14:] != lines2[14:]:
                    print("32-bit")
                    print("want: " + lines1[14:] + "out: " + lines2[14:])
                    return False
            return True


def test(name, func, n):
    for _ in range(0, n):
        line, high = func(name, n)
        if build(line) != 0:
            print("Build failed!")
            return False
        if not diff(high):
            return False
    return True


def fd_fj_s(name, n):
    line = "la.local $t0, fj_s\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, False


def fd_fj_d(name, n):
    line = "la.local $t0, fj_d\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, True


def fd_fj_fk_s(name, n):
    line = "la.local $t0, fj_s\n    "
    line += "la.local $t1, fk_s\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"fld.s $f2, $t1, {4 * n}\n    "
    line += f"{name} $f0, $f1, $f2\n"
    return line, False


def fd_fj_fk_d(name, n):
    line = "la.local $t0, fj_d\n    "
    line += "la.local $t1, fk_d\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"fld.d $f2, $t1, {8 * n}\n    "
    line += f"{name} $f0, $f1, $f2\n"
    return line, True


def fd_fj_fk_fa_s(name, n):
    line = "la.local $t0, fj_s\n    "
    line += "la.local $t1, fk_s\n    "
    line += "la.local $t2, fa_s\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"fld.s $f2, $t1, {4 * n}\n    "
    line += f"fld.s $f3, $t2, {4 * n}\n    "
    line += f"{name} $f0, $f1, $f2, $f3\n"
    return line, False


def fd_fj_fk_fa_d(name, n):
    line = "la.local $t0, fj_d\n    "
    line += "la.local $t1, fk_d\n    "
    line += "la.local $t2, fa_d\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"fld.d $f2, $t1, {8 * n}\n    "
    line += f"fld.d $f3, $t2, {8 * n}\n    "
    line += f"{name} $f0, $f1, $f2, $f3\n"
    return line, True


def fd_fj_s_d(name, n):
    line = "la.local $t0, fj_d\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, False


def fd_fj_d_s(name, n):
    line = "la.local $t0, fj_s\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, True


def fd_fj_w_s(name, n):
    line = "la.local $t0, fj_s\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, False


def fd_fj_w_d(name, n):
    line = "la.local $t0, fj_d\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, False


def fd_fj_l_s(name, n):
    line = "la.local $t0, fj_s\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, True


def fd_fj_l_d(name, n):
    line = "la.local $t0, fj_d\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, True


def fd_fj_s_w(name, n):
    line = "la.local $t0, fj_w\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, False


def fd_fj_s_l(name, n):
    line = "la.local $t0, fj_l\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, False


def fd_fj_d_w(name, n):
    line = "la.local $t0, fj_w\n    "
    line += f"fld.s $f1, $t0, {4 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, True


def fd_fj_d_l(name, n):
    line = "la.local $t0, fj_l\n    "
    line += f"fld.d $f1, $t0, {8 * n}\n    "
    line += f"{name} $f0, $f1\n"
    return line, True


insts = [
   # { "name": "fadd.s",         "func": fd_fj_fk_s },
   # { "name": "fadd.d",         "func": fd_fj_fk_d },
   # { "name": "fsub.s",         "func": fd_fj_fk_s },
   # { "name": "fsub.d",         "func": fd_fj_fk_d },
   # { "name": "fmul.s",         "func": fd_fj_fk_s },
   # { "name": "fmul.d",         "func": fd_fj_fk_d },
   # { "name": "fdiv.s",         "func": fd_fj_fk_s },
   # { "name": "fdiv.d",         "func": fd_fj_fk_d },
    { "name": "fmadd.s",        "func": fd_fj_fk_fa_s },
   # { "name": "fmadd.d",        "func": fd_fj_fk_fa_d },
   # { "name": "fmsub.s",        "func": fd_fj_fk_fa_s },
   # { "name": "fmsub.d",        "func": fd_fj_fk_fa_d },
   # { "name": "fnmadd.s",       "func": fd_fj_fk_fa_s },
   # { "name": "fnmadd.d",       "func": fd_fj_fk_fa_d },
   # { "name": "fnmsub.s",       "func": fd_fj_fk_fa_s },
   # { "name": "fnmsub.d",       "func": fd_fj_fk_fa_d },
   # { "name": "fmax.s",         "func": fd_fj_fk_s },
   # { "name": "fmax.d",         "func": fd_fj_fk_d },
   # { "name": "fmin.s",         "func": fd_fj_fk_s },
   # { "name": "fmin.d",         "func": fd_fj_fk_d },
   # { "name": "fmaxa.s",        "func": fd_fj_fk_s },
   # { "name": "fmaxa.d",        "func": fd_fj_fk_d },
   # { "name": "fmina.s",        "func": fd_fj_fk_s },
   # { "name": "fmina.d",        "func": fd_fj_fk_d },
   # { "name": "fabs.s",         "func": fd_fj_s },
   # { "name": "fabs.d",         "func": fd_fj_d },
   # { "name": "fneg.s",         "func": fd_fj_s },
   # { "name": "fneg.d",         "func": fd_fj_d },
   # { "name": "fsqrt.s",        "func": fd_fj_s },
   # { "name": "fsqrt.d",        "func": fd_fj_d },
   # { "name": "frecip.s",       "func": fd_fj_s },
   # { "name": "frecip.d",       "func": fd_fj_d },
   # { "name": "frsqrt.s",       "func": fd_fj_s },
   # { "name": "frsqrt.d",       "func": fd_fj_d },
   # { "name": "fscaleb.s",      "func": fd_fj_fk_s },
   # { "name": "fscaleb.d",      "func": fd_fj_fk_d },
   # { "name": "flogb.s",        "func": fd_fj_s },
   # { "name": "flogb.d",        "func": fd_fj_d },
   # { "name": "fcopysign.s",    "func": fd_fj_fk_s },
   # { "name": "fcopysign.d",    "func": fd_fj_fk_d },
   # { "name": "fclass.s",       "func": fd_fj_s },
   # { "name": "fclass.d",       "func": fd_fj_d },
   # { "name": "fcvt.s.d",       "func": fd_fj_s_d },
   # { "name": "fcvt.d.s",       "func": fd_fj_d_s },
   # { "name": "ftintrm.w.s",    "func": fd_fj_w_s },
   # { "name": "ftintrm.w.d",    "func": fd_fj_w_d },
   # { "name": "ftintrm.l.s",    "func": fd_fj_l_s },
   # { "name": "ftintrm.l.d",    "func": fd_fj_l_d },
   # { "name": "ftintrp.w.s",    "func": fd_fj_w_s },
   # { "name": "ftintrp.w.d",    "func": fd_fj_w_d },
   # { "name": "ftintrp.l.s",    "func": fd_fj_l_s },
   # { "name": "ftintrp.l.d",    "func": fd_fj_l_d },
   # { "name": "ftintrz.w.s",    "func": fd_fj_w_s },
   # { "name": "ftintrz.w.d",    "func": fd_fj_w_d },
   # { "name": "ftintrz.l.s",    "func": fd_fj_l_s },
   # { "name": "ftintrz.l.d",    "func": fd_fj_l_d },
   # { "name": "ftintrne.w.s",   "func": fd_fj_w_s },
   # { "name": "ftintrne.w.d",   "func": fd_fj_w_d },
   # { "name": "ftintrne.l.s",   "func": fd_fj_l_s },
   # { "name": "ftintrne.l.d",   "func": fd_fj_l_d },
   # { "name": "ftint.w.s",      "func": fd_fj_w_s },
   # { "name": "ftint.w.d",      "func": fd_fj_w_d },
   # { "name": "ftint.l.s",      "func": fd_fj_l_s },
   # { "name": "ftint.l.d",      "func": fd_fj_l_d },
   # { "name": "ffint.s.w",      "func": fd_fj_s_w },
   # { "name": "ffint.s.l",      "func": fd_fj_s_l },
   # { "name": "ffint.d.w",      "func": fd_fj_d_w },
   # { "name": "ffint.d.l",      "func": fd_fj_d_l },
   # { "name": "frint.s",        "func": fd_fj_s },
   # { "name": "frint.d",        "func": fd_fj_d }
]

n = 24
for inst in insts:
    if not test(inst["name"], inst["func"], n):
        print(f"{inst['name']} failed")
        break
    else:
        print(f"{inst['name']} passed")
