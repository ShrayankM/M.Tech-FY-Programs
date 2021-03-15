#include<bits/stdc++.h>
#include<omp.h>

using namespace std;


const int N = 1024;
int A[N][N]; 
int B[N][N];
int C[N][N];

void sequential_multiply() {
    int dot;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            dot = 0;
            for (int k = 0; k < N; k++) {
                dot += A[i][k] * B[k][j];
            }
            C[i][j] = dot;
        }
    }
}

int main() {

    //* Initialize Matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = B[i][j] = 1;
        }
    }

    double dtime;
    dtime = omp_get_wtime();
    sequential_multiply();
    dtime = omp_get_wtime() - dtime;
    printf("Sequential Time = %f secs\n", dtime);

    return 0;
}