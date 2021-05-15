#include<stdio.h>
#include<cuda.h>
#define row1 5
#define col1 5
#define row2 5
#define col2 5

__global__ void matproduct(int *l,int *m, int *n)
{
    int x=blockIdx.x;
    int y=blockIdx.y;
    int k;
  
    n[col2*y+x]=0;
    for(k=0;k<col1;k++)
    {
        n[col2*y+x]=n[col2*y+x]+l[col1*y+k]*m[col2*k+x];
    }
}

int main()
{
    int a[row1][col1];
    int b[row2][col2];
    int c[row1][col2];

    int *d,*e,*f;
    int i,j;
 
    clock_t start, end;
    double cpu_time_used; 
 
    start = clock();    
    for(i=0;i<row1;i++)
    {
        for(j=0;j<col1;j++)
            {
                a[i][j] = 1;
                b[i][j] = 1;
            }
    }    

    cudaMalloc((void **)&d,row1*col1*sizeof(int));
    cudaMalloc((void **)&e,row2*col2*sizeof(int));
    cudaMalloc((void **)&f,row1*col2*sizeof(int));

    cudaMemcpy(d,a,row1*col1*sizeof(int),cudaMemcpyHostToDevice);
    cudaMemcpy(e,b,row2*col2*sizeof(int),cudaMemcpyHostToDevice);

    dim3 grid(col2,row1);       //Here we are defining two dimensional Grid(collection of blocks) structure.
                                  // Syntax is dim3 grid(no. of columns,no. of rows)

    matproduct<<<grid,1>>>(d,e,f);

    cudaMemcpy(c,f,row1*col2*sizeof(int),cudaMemcpyDeviceToHost);

    cudaDeviceSynchronize();

    for (int i = 0; i < row1; i++) {
        for (int j = 0; j < col2; j++) {
            printf("%d ", c[i][j]);
        }
        printf("\n");
    }
    
 
     end = clock();
     cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;  
     printf (" time =  %f s\n", cpu_time_used );

    cudaFree(d);
    cudaFree(e);
    cudaFree(f);

    return 0;
}