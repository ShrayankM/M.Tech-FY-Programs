#include <stdio.h>
#include <stdlib.h> 
#include <time.h>

#define ROWS_A 2000
#define COLS_A 2000

#define ROWS_B 2000
#define COLS_B 2000

#define MAX 128

void displayMatrix(int* a, int r, int c) {
    
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            printf("%d ", a[i * c + j]);
        }
        printf("\n");
    }
}

int main(int argc, char* argv[]) {


    int* A = (int*)malloc(ROWS_A * COLS_A * sizeof(int));
    int* B = (int*)malloc(ROWS_B * COLS_B * sizeof(int));

    int* C = (int*)malloc(ROWS_A * COLS_B * sizeof(int));

    //* Initializing Matrix A
    for (int i = 0; i < ROWS_A; i++) {
        for (int j = 0; j < COLS_A; j++) {
            A[i * COLS_A + j] = rand() % MAX + 1;
        }
    }

    //* Initializing Matrix B
    for (int i = 0; i < ROWS_B; i++) {
        for (int j = 0; j < COLS_B; j++) {
            B[i * COLS_B + j] = rand() % MAX + 1;
        }
    }

    clock_t begin = clock();
    for (int i = 0; i < ROWS_A; i++) {
        for (int j = 0; j < COLS_B; j++) {
            int sum = 0;
            for (int k = 0; k < COLS_A; k++) {
                sum += A[i * COLS_A + k] * B[k * COLS_B + j];
            }
            C[i * COLS_B + j] = sum;
        }
    }

    clock_t end = clock();
    printf("The elapsed time is %f seconds\n", (double)(end - begin) / CLOCKS_PER_SEC);

    // displayMatrix(C, ROWS_A, COLS_B);

    return 0;
}