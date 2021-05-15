#include <stdio.h>
#include <stdlib.h>
#include <cuda.h>
#include <time.h>

#define ROWS_A 5000
#define COLS_A 5000

#define ROWS_B 5000
#define COLS_B 5000

#define MAX 128

__global__ void multiplyMatrices(int* a, int *b, int* c, int ra, int ca, int rb, int cb) {

    int threadId = blockIdx.x * blockDim.x + threadIdx.x;

    int rno, cno;
    rno = cno = threadId / ra;

    int sum = 0;
    for (int i = 0; i < ca; i++) {
        sum += a[rno * ca + i] * b[i * cb + cno];
    }

    c[rno * cb + (threadId % ra)] = sum;
}

void displayMatrix(int* a, int r, int c) {
    
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            printf("%d ", a[i * c + j]);
        }
        printf("\n");
    }
}

int main(int argc, char* argv[]) {

    cudaError_t err = cudaSuccess;
    cudaEvent_t start, stop;
    float elapsed_time_ms;

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

    int* hA;
    int* hB;

    int* hC;

    if (cudaMalloc(&hA, ROWS_A * COLS_A * sizeof(int)) != cudaSuccess) {
        printf("Cannot Allocate Memory for A on GPU\n");
        return 0;
    }

    if (cudaMalloc(&hB, ROWS_B * COLS_B * sizeof(int)) != cudaSuccess) {
        printf("Cannot Allocate Memory for B on GPU\n");
        return 0;
    }

    if (cudaMalloc(&hC, ROWS_A * COLS_B * sizeof(int)) != cudaSuccess) {
        printf("Cannot Allocate Memory for C on GPU\n");
        return 0;
    }

    if (cudaMemcpy(hA, A, ROWS_A * COLS_A * sizeof(int), cudaMemcpyHostToDevice) != cudaSuccess) {
        printf("Cannot Data from A on CPU to GPU\n");
        return 0;
    }

    if (cudaMemcpy(hB, B, ROWS_B * COLS_B * sizeof(int), cudaMemcpyHostToDevice) != cudaSuccess) {
        printf("Cannot Data from B on CPU to GPU\n");
        return 0;
    }

    int threadsPerBlock = 1024;
    int blocks = (ROWS_A * COLS_A + threadsPerBlock - 1) / threadsPerBlock;
    printf("CUDA kernel launch with %d blocks of %d threads\n", blocks, threadsPerBlock);

    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);

    multiplyMatrices<<<blocks, threadsPerBlock>>>(hA, hB, hC, ROWS_A, COLS_A, ROWS_B, COLS_B);
    err = cudaGetLastError();
 
    if (err != cudaSuccess) {
        printf("Failed to launch multiplyMatrices kernel (error code)!\n");
        return 0;
    }

    if (cudaMemcpy(C, hC, ROWS_A * COLS_B * sizeof(int), cudaMemcpyDeviceToHost) != cudaSuccess) {
        printf("Cannot copy multiplied matrix from GPU to CPU\n");
        return 0;
    }

    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&elapsed_time_ms, start, stop);

    printf("The elapsed time is %f seconds\n", elapsed_time_ms / 1000);

    // displayMatrix(C, ROWS_A, COLS_B);

    return 0;
}