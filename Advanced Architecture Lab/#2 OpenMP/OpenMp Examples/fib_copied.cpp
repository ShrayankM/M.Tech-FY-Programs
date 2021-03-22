/* OpenMP code to compute Fibonacci */
#include <stdlib.h>
#include <stdio.h>
#include "omp.h"

static int fib(int);

int main()
{
    int nthreads, tid;
    int n = 30;

    double dtime = omp_get_wtime();
    #pragma omp parallel num_threads(4) private(tid)
    {
        #pragma omp single
        {
            tid = omp_get_thread_num();
            printf("Hello world from (%d)\n", tid);
            printf("Fib(%d) = %d by %d\n", n, fib(n), tid);
        }
    }

    printf("Time = (%f)\n", omp_get_wtime() - dtime);
}

static int fib(int n){
        int i, j, id;
        if (n < 2)
            return n;
        #pragma omp task shared(i) private (id)
        {
            i = fib(n - 1);
        }
        
        #pragma omp task shared(j) private(id)
        {
            j = fib(n - 2);
        }

        #pragma omp taskwait
        return (i + j);
}