#include <stdio.h>
#include <stdlib.h>

#define N 10
#define MAX 10

int array[N];

void merge(int array[], int L, int M, int H) {
    int* C = (int*)malloc((H - L + 1) * sizeof(int));

    int i = L, j = M + 1;
    int k = 0;
    while (i <= M && j <= H) {
        if (array[i] < array[j]) C[k++] = array[i++];
        else                     C[k++] = array[j++];
    }

    while (i <= M) C[k++] = array[i++];
    while (j <= H) C[k++] = array[j++];

    for (int i = L; i <= H; i++)
        array[i] = C[i - L];
}

void mergesort(int array[], int L, int H) {
    if (L < H) {
        int M = (L + H)/2;
        mergesort(array, L, M);
        mergesort(array, M + 1, H);
        merge(array, L, M, H);
    }
}

int main(int argc, char* argv[]) {

    for (int i = 0; i < N; i++) {
        array[i] = (rand() % (MAX)) + 1;
    }

    mergesort(array, 0, N - 1);

    for (int i = 0; i < N; i++) 
        printf("%d\t", array[i]);
    printf("\n");
    return 0;
}