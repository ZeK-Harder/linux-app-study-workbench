#include <stdio.h>
#include <stdlib.h>

static int sum_to(int n) {
    int s = 0;
    for (int i = 1; i <= n; i++) {
        s += i;
    }
    return s;
}

int main(int argc, char **argv) {
    int n = (argc > 1) ? atoi(argv[1]) : 10;
    if (n <= 0) {
        fprintf(stderr, "usage: %s [positive int]\n", argv[0]);
        return 1;
    }

    printf("Hello, Linux!\n");
    printf("sum(1..%d) = %d\n", n, sum_to(n));
    return 0;
}
