#include <stdio.h>
#include <cuda.h>

__global__ void sayHello()
{
    printf("Basic Info: BlockId = %d,  ThreadId in block =  %d\n", blockIdx.x, threadIdx.x);
    printf("Hello World from the GPU [unique thread no. = %d]\n", blockIdx.x * blockDim.x + threadIdx.x);
}

int main()
{

    sayHello<<<3, 2>>>();
    printf("Hello World from the CPU\n");
    cudaDeviceSynchronize();

    return EXIT_SUCCESS;
}
