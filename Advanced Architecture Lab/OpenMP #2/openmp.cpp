#include<bits/stdc++.h>
#include<omp.h>

using namespace std;


const int N = 1024;
int A[N][N]; 
int B[N][N];
int C[N][N];

void displayMatrix(int temp[N][N]) {
    // for (int i = 0; i < N; i++) {
    //     for (int j = 0; j < N; j++) {
    //         cout << temp[i][j] << " ";
    //     }
    //     cout << "\n";
    // }

    cout << temp[0][0] << " -- " << temp[N - 1][N - 1] << "\n";
}

void parallel_multiply() {
    #pragma omp parallel 
    {
        int i, j, k;
        #pragma omp for 
        for (i = 0; i < N; i++) {
            for (j = 0; j < N; j++) {
                int dot = 0;
                for (k = 0; k < N; k++) {
                    dot += A[i][k] * B[k][j];
                }
                C[i][j] = dot;
            }
        }
    }
}

int main() {

    //* Initialize Matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = i - j;
            B[i][j] = i + j;
        }
    }

    double dtime;

    dtime = omp_get_wtime();
    parallel_multiply();
    dtime = omp_get_wtime() - dtime;
    printf("Parallel Time = %f secs\n", dtime);

    displayMatrix(C);
    return 0;
}