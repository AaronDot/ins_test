void print(char *s, int n);

unsigned long long regs[32 + 32 + 4 + 8];

int my_strlen(char *s)
{
    char *t = s;
    while (*s != '\0')
        s++;
    return s - t;
}

void my_puts(char *s)
{
    print(s, my_strlen(s));
}

void my_itoa(char *s, unsigned long long n, int base)
{
    char t[20];
    char a[] = { '0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };
    int i = 0;
    if (base == 16) {
#if 0
        *s++ = '0';
        *s++ = 'x';
#endif
    } else if ((long) n < 0) {
        *s++ = '-';
        n = -n;
    }
    do {
        t[i++] = a[n % base];
        n /= base;
    } while (n != 0);
    while (--i >= 0)
        *s++ = t[i];
    *s = '\0';
}

void widen(char *dst, char *src, int len)
{
    //*dst++ = *src++; // '0'
    //*dst++ = *src++; // 'x'
    for (int i = my_strlen(src); i < len; i++)
        *dst++ = '0';
    while ((*dst++ = *src++) != '\0')
        continue;
}

int show(unsigned long long *regs)
{
#if 0
    char s[20], t[20];
    for (int i = 0; i < 32; i++) {
        my_puts("r");
        my_itoa(s, i, 10);
        my_puts(s);
        my_puts(":\t");
        my_itoa(s, regs[i], 16);
        widen(t, s, 16);
        my_puts(t);
        my_puts("\n");
    }
    for (int i = 0; i < 32; i++) {
        my_puts("f");
        my_itoa(s, i, 10);
        my_puts(s);
        my_puts(":\t");
        my_itoa(s, regs[i + 32], 16);
        widen(t, s, 16);
        my_puts(t);
        my_puts("\n");
    }
    for (int i = 0; i < 4; i++) {
        my_puts("fcsr");
        my_itoa(s, i, 10);
        my_puts(s);
        my_puts(":\t");
        my_itoa(s, regs[i + 64], 16);
        widen(t, s, 8);
        my_puts(t);
        my_puts("\n");
    }
    for (int i = 0; i < 8; i++) {
        my_puts("fcc");
        my_itoa(s, i, 10);
        my_puts(s);
        my_puts(":\t");
        my_itoa(s, regs[i + 68], 16);
        my_puts(s);
        my_puts("\n");
    }
    for (int i = 0; i < 32; i++) {
        my_puts("rv");
        my_itoa(s, i, 10);
        my_puts(s);
        my_puts(":\t");
        my_itoa(s, regs[i + 76], 16);
        widen(t, s, 16);
        my_puts(t);
        my_puts("\n");
    }
    return 0;
#else
    char s[20], t[20];
    my_puts("f");
    my_itoa(s, 0, 10);
    my_puts(s);
    my_puts(":\t");
    my_itoa(s, regs[32], 16);
    widen(t, s, 16);
    my_puts(t);
    my_puts("\n");
    my_puts("fcsr");
    my_itoa(s, 0, 10);
    my_puts(s);
    my_puts(":\t");
    my_itoa(s, regs[64], 16);
    widen(t, s, 8);
    my_puts(t);
    my_puts("\n");

    for (int i = 0; i < 8; i++) {
        my_puts("fcc");
        my_itoa(s, i, 10);
        my_puts(s);
        my_puts(":\t");
        my_itoa(s, regs[i + 68], 16);
        my_puts(s);
        my_puts("\n");
    }
    return 0;
#endif
}
