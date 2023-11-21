
const float fj_s[] = {
    0,         456.25,   3,          -1,
    1384.5,    -7.25,    1000000000, -5786.5,
    1752,      0.015625, 0.03125,    -248562.75,
    -45786.5,  456,      34.03125,   45786.75,
    1752065,   107,      -45667.25,  -7,
    -347856.5, 356047.5, -1.0,       23.0625
};

const double fj_d[] = {
    0,         456.25,   3,          -1,
    1384.5,    -7.25,    1000000000, -5786.5,
    1752,      0.015625, 0.03125,    -248562.75,
    -45786.5,  456,      34.03125,   45786.75,
    1752065,   107,      -45667.25,  -7,
    -347856.5, 356047.5, -1.0,       23.0625
};

const float fk_s[] = {
    -4578.5, 456.25,   34.03125, 4578.75,
    175,     107,      -456.25,  -7.25,
    -3478.5, 356.5,    -1.0,     23.0625,
    0,       456.25,   3,        -1,
    1384.5,  -7,       100,      -5786.5,
    1752,    0.015625, 0.03125,  -248562.75
};

const double fk_d[] = {
    -45786.5,  456.25,   34.03125,   45786.75,
    1752065,   107,      -45667.25,  -7.25,
    -347856.5, 356047.5, -1.0,       23.0625,
    0,         456.25,   3,          -1,
    1384.5,    -7,       1000000000, -5786.5,
    1752,      0.015625, 0.03125,    -248562.75
};

const float fa_s[] = {
    -347856.5,  356047.5,  -1.0,       23.0625,
    1752,       0.015625,  0.03125,    -248562.75,
    1384.5,     -7.25,     1000000000, -5786.5,
    -347856.75, 356047.75, -1.0,       23.03125,
    0,          456.25,    3,          -1,
    -45786.5,   456,       34.03125,   45786.03125,
};

const double fa_d[] = {
    -347856.5,  356047.5,  -1.0,       23.0625,
    1752,       0.015625,  0.03125,    -248562.75,
    1384.5,     -7.25,     1000000000, -5786.5,
    -347856.75, 356047.75, -1.0,       23.03125,
    0,          456.25,    3,          -1,
    -45786.5,   456,       34.03125,   45786.03125,
};

const int fj_w[] = {
    0,          456,        3,          -1,
    0xffffffff, 356,        1000000000, -5786,
    1752,       24575,      10,         -248562,
    -45786,     456,        34,         45786,
    1752065,    107,        -45667,     -7,
    -347856,    0x80000000, 0xfffffff,  23,
};

const long fj_l[] = {
    18,         25,         3,          -1,
    0xffffffff, 356,        1000000,    -5786,
    -1,         24575,      10,         -125458,
    -486,       456,        34,         45786,
    0,          1700000,    -45667,     -7,
    -347856,    0x80000000, 0xfffffff,  23,
};

unsigned long long mem_j[32] = {
   0x0000000000000000ull, 0x0000000000000000ull,
   0xffffffffffffffffull, 0xffffffffffffffffull,
   0x0000000080000000ull, 0x8000000000000000ull,
   0x8000800080008000ull, 0x7fff7fff7fff7fffull,
   0x8080808080808080ull, 0x8080808080808080ull,
   0x7070707070707070ull, 0x7070707070707070ull,
   0x7f7f7f7f7f7f7f7full, 0x7f7f7f7f7f7f7f7full,
   0x0706050403020100ull, 0x0f0e0d0c0b0a0908ull,
   0x77665544332211ffull, 0xeeddccbbaa998877ull,
   0x0000000000000001ull, 0x00000000000001ffull,
   0x0000000000000001ull, 0x00000000000000ffull,
   0xffffffffffffffffull, 0x0000000000000000ull,
   0x0000000100000001ull, 0x0000000100000001ull,
   0x1234567890abcdefull, 0xfedbca9876543210ull,
   0x0403020114131211ull, 0x2423222134333231ull,
   0x8483828194939291ull, 0xa4a3a2a1b4b3b2b1ull,
};

unsigned long long mem_k[32] = {
   0x0000000000000000ull, 0x0000000000000000ull,
   0xffffffffffffffffull, 0xffffffffffffffffull,
   0x0000000080000000ull, 0x8000000000000000ull,
   0x8000800080008000ull, 0x7fff7fff7fff7fffull,
   0x8080808080808080ull, 0x8080808080808080ull,
   0x7070707070707070ull, 0x7070707070707070ull,
   0x7f7f7f7f7f7f7f7full, 0x7f7f7f7f7f7f7f7full,
   0x0706050403020100ull, 0x0f0e0d0c0b0a0908ull,
   0x77665544332211ffull, 0xeeddccbbaa998877ull,
   0x0000000000000001ull, 0x00000000000001ffull,
   0x0000000000000001ull, 0x00000000000000ffull,
   0xffffffffffffffffull, 0x0000000000000000ull,
   0x0000000100000001ull, 0x0000000100000001ull,
   0x1234567890abcdefull, 0xfedbca9876543210ull,
   0x0403020114131211ull, 0x2423222134333231ull,
   0x8483828194939291ull, 0xa4a3a2a1b4b3b2b1ull,
};