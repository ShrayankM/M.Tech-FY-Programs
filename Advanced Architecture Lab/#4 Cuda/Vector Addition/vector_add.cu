#include <stdio.h>
#include <stdlib.h>
#include <cuda.h>
#include <time.h>

__global__ void addVectors(int* a, int* b, int N) {
    int id = blockIdx.x * blockDim.x + threadIdx.x;

    if (id < N) {
        a[id] = a[id] + b[id];
    }
}


int main() {

    int N = 4096 * 4096;
    int MAX = 4096;

    cudaError_t err = cudaSuccess;
    //* Normal vector for initialization
    int* a = (int*)malloc(sizeof(int) * N);
    int* b = (int*)malloc(sizeof(int) * N);

    for (int i = 0; i < N; i++) {
        a[i] = (rand() % MAX) + 1;
        b[i] = (rand() % MAX) + 1;
    }

    printf("Vector Addition of %d elements\n", N);

    // * DS for the GPU
    int* ga;
    int* gb;

    //* Allocating memory for vectors on the GPU
    if (cudaMalloc(&ga, sizeof(int) * N) != cudaSuccess) {
        printf("Cannot Allocate Memory for A on GPU\n");
        return 0;
    }

    if (cudaMalloc(&gb, sizeof(int) * N) != cudaSuccess) {
        printf("Cannot Allocate Memory for B on GPU\n");
        return 0;
    }

    //* Copying data contents from CPU to GPU
    if (cudaMemcpy(ga, a, sizeof(int) * N, cudaMemcpyHostToDevice) != cudaSuccess) {
        printf("Cannot Data from A on CPU to GPU\n");
        return 0;
    }

    if (cudaMemcpy(gb, b, sizeof(int) * N, cudaMemcpyHostToDevice) != cudaSuccess) {
        printf("Cannot Data from B on CPU to GPU\n");
        return 0;
    }

    int threadsPerBlock = 1024;
    int blocks =(N + threadsPerBlock - 1) / threadsPerBlock;
    printf("CUDA kernel launch with %d blocks of %d threads\n", blocks, threadsPerBlock);

    clock_t begin = clock();
    addVectors<<<blocks, threadsPerBlock>>>(ga, gb, N);
    err = cudaGetLastError();
 
    if (err != cudaSuccess) {
        printf("Failed to launch addVectors kernel (error code)!\n");
        return 0;
    }
    
    if (cudaMemcpy(a, ga, sizeof(int) * N, cudaMemcpyDeviceToHost) != cudaSuccess) {
        printf("Cannot copy added vector from GPU to CPU\n");
        return 0;
    }

    clock_t end = clock();
    printf("The elapsed time is %f seconds\n", (double)(end - begin) / CLOCKS_PER_SEC);

    // for (int i = 0; i < N; i++) 
    //     printf("%d ", a[i]);
    // printf("\n");

    cudaFree(ga);
    cudaFree(gb);

    free(a);
    free(b);

    return 0;
}