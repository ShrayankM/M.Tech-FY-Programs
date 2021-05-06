#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {

    int N = 4096 * 4096;
    int MAX = 500;

    int* a = (int*)malloc(sizeof(int) * N);
    int* b = (int*)malloc(sizeof(int) * N);

    for (int i = 0; i < N; i++) {
        a[i] = (rand() % MAX) + 1;
        b[i] = (rand() % MAX) + 1;
    }

    printf("Vector Addition of %d elements\n", N);

    clock_t begin = clock();

    for (int i = 0; i < N; i++) 
        a[i] = a[i] + b[i];

    clock_t end = clock();
    printf("The elapsed time is %f seconds\n", (double)(end - begin) / CLOCKS_PER_SEC);

    return 0;
}