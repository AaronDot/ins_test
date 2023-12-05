.text
.globl _start
_start:
    li.w       $t0, 0x0
    movgr2cf   $fcc0, $t0
    movgr2cf   $fcc1, $t0
    movgr2cf   $fcc2, $t0
    movgr2cf   $fcc3, $t0
    movgr2cf   $fcc4, $t0
    movgr2cf   $fcc5, $t0
    movgr2cf   $fcc6, $t0
    movgr2cf   $fcc7, $t0

    nop

dump:
#    la.local   $r21,   regs
#    st.d       $r0,  $r21,  0
#    st.d       $r1,  $r21,  8
#    st.d       $r2,  $r21,  16
#    st.d       $r3,  $r21,  24
#    st.d       $r4,  $r21,  32
#    st.d       $r5,  $r21,  40
#    st.d       $r6,  $r21,  48
#    st.d       $r7,  $r21,  56
#    st.d       $r8,  $r21,  64
#    st.d       $r9,  $r21,  72
#    st.d       $r10, $r21,  80
#    st.d       $r11, $r21,  88
#    st.d       $r12, $r21,  96
#    st.d       $r13, $r21,  104
#    st.d       $r14, $r21,  112
#    st.d       $r15, $r21,  120
#    st.d       $r16, $r21,  128
#    st.d       $r17, $r21,  136
#    st.d       $r18, $r21,  144
#    st.d       $r19, $r21,  152
#    st.d       $r20, $r21,  160
#    st.d       $r21, $r21,  168
#    st.d       $r22, $r21,  176
#    st.d       $r23, $r21,  184
#    st.d       $r24, $r21,  192
#    st.d       $r25, $r21,  200
#    st.d       $r26, $r21,  208
#    st.d       $r27, $r21,  216
#    st.d       $r28, $r21,  224
#    st.d       $r29, $r21,  232
#    st.d       $r30, $r21,  240
#    st.d       $r31, $r21,  248
#    fst.d      $f0,  $r21,  256
#    fst.d      $f1,  $r21,  264
#    fst.d      $f2,  $r21,  272
#    fst.d      $f3,  $r21,  280
#    fst.d      $f4,  $r21,  288
#    fst.d      $f5,  $r21,  296
#    fst.d      $f6,  $r21,  304
#    fst.d      $f7,  $r21,  312
#    fst.d      $f8,  $r21,  320
#    fst.d      $f9,  $r21,  328
#    fst.d      $f10, $r21,  336
#    fst.d      $f11, $r21,  344
#    fst.d      $f12, $r21,  352
#    fst.d      $f13, $r21,  360
#    fst.d      $f14, $r21,  368
#    fst.d      $f15, $r21,  376
#    fst.d      $f16, $r21,  384
#    fst.d      $f17, $r21,  392
#    fst.d      $f18, $r21,  400
#    fst.d      $f19, $r21,  408
#    fst.d      $f20, $r21,  416
#    fst.d      $f21, $r21,  424
#    fst.d      $f22, $r21,  432
#    fst.d      $f23, $r21,  440
#    fst.d      $f24, $r21,  448
#    fst.d      $f25, $r21,  456
#    fst.d      $f26, $r21,  464
#    fst.d      $f27, $r21,  472
#    fst.d      $f28, $r21,  480
#    fst.d      $f29, $r21,  488
#    fst.d      $f30, $r21,  496
#    fst.d      $f31, $r21,  504
#    movfcsr2gr $t0,  $r0
#    movfcsr2gr $t1,  $r1
#    movfcsr2gr $t2,  $r2
#    movfcsr2gr $t3,  $r3
#    st.d       $t0,  $r21,  512
#    st.d       $t1,  $r21,  520
#    st.d       $t2,  $r21,  528
#    st.d       $t3,  $r21,  536
#    movcf2gr   $t0,  $fcc0
#    andi       $t0,  $t0, 1
#    movcf2gr   $t1,  $fcc1
#    andi       $t1,  $t1, 1
#    movcf2gr   $t2,  $fcc2
#    andi       $t2,  $t2, 1
#    movcf2gr   $t3,  $fcc3
#    andi       $t3,  $t3, 1
#    movcf2gr   $t4,  $fcc4
#    andi       $t4,  $t4, 1
#    movcf2gr   $t5,  $fcc5
#    andi       $t5,  $t5, 1
#    movcf2gr   $t6,  $fcc6
#    andi       $t6,  $t6, 1
#    movcf2gr   $t7,  $fcc7
#    andi       $t7,  $t7, 1
#    st.d       $t0,  $r21,  544
#    st.d       $t1,  $r21,  552
#    st.d       $t2,  $r21,  560
#    st.d       $t3,  $r21,  568
#    st.d       $t4,  $r21,  576
#    st.d       $t5,  $r21,  584
#    st.d       $t6,  $r21,  592
#    st.d       $t7,  $r21,  600
#    vst        $vr0, $r21,  608
#    vst        $vr1, $r21,  624
#    vst        $vr2, $r21,  640
#    vst        $vr3, $r21,  656
#    vst        $vr4, $r21,  672
#    vst        $vr5, $r21,  688
#    vst        $vr6, $r21,  704
#    vst        $vr7, $r21,  720
#    vst        $vr8, $r21,  736
#    vst        $vr9, $r21,  752
#    vst        $vr10, $r21,  768
#    vst        $vr11, $r21,  784
#    vst        $vr12, $r21,  800
#    vst        $vr13, $r21,  816
#    vst        $vr14, $r21,  832
#    vst        $vr15, $r21,  848
#    vst        $vr16, $r21,  864
#    vst        $vr17, $r21,  880
#    vst        $vr18, $r21,  896
#    vst        $vr19, $r21,  912
#    vst        $vr20, $r21,  928
#    vst        $vr21, $r21,  944
#    vst        $vr22, $r21,  960
#    vst        $vr23, $r21,  976
#    vst        $vr24, $r21,  992
#    vst        $vr25, $r21,  1008
#    vst        $vr26, $r21,  1024
#    vst        $vr27, $r21,  1040
#    vst        $vr28, $r21,  1056
#    vst        $vr29, $r21,  1072
#    vst        $vr30, $r21,  1088
#    vst        $vr31, $r21,  1104

    la.local   $r21, regs
    vst        $vr0, $r21,  0
    vst        $vr1, $r21,  16
    vst        $vr2, $r21,  32
    movcf2gr   $t0,  $fcc0
    andi       $t0,  $t0, 1
    movcf2gr   $t1,  $fcc1
    andi       $t1,  $t1, 1
    movcf2gr   $t2,  $fcc2
    andi       $t2,  $t2, 1
    movcf2gr   $t3,  $fcc3
    andi       $t3,  $t3, 1
    movcf2gr   $t4,  $fcc4
    andi       $t4,  $t4, 1
    movcf2gr   $t5,  $fcc5
    andi       $t5,  $t5, 1
    movcf2gr   $t6,  $fcc6
    andi       $t6,  $t6, 1
    movcf2gr   $t7,  $fcc7
    andi       $t7,  $t7, 1
    st.d       $t0,  $r21,  48
    st.d       $t1,  $r21,  56
    st.d       $t2,  $r21,  64
    st.d       $t3,  $r21,  72
    st.d       $t4,  $r21,  80
    st.d       $t5,  $r21,  88
    st.d       $t6,  $r21,  96
    st.d       $t7,  $r21,  104
    st.d       $r20, $r21,  112
    move       $a0,  $r21
    bl         show

exit:
    li.w    $a7, 93   // n = __NR_exit
    syscall 0         // exit(ret)

.globl print
print:
    move    $a2, $a1  // l
    move    $a1, $a0  // s
    li.w    $a0, 2    // f = stderr
    li.w    $a7, 64   // n = __NR_write
    syscall 0         // write(f, s, l)
    jr      $ra
