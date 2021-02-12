#include<bits/stdc++.h> 
#include<pthread.h>
using namespace std; 

const int N = 1024;
const int n = 32;

const int T = 1024;

double get_seconds() {
    return (double) clock();
}


int A[N][N], B[N][N], C[N][N], D[N][N];

void displayMatrix(int temp[N][N]) {
    // for (int i = 0; i < N; i++) {
    //     for (int j = 0; j < N; j++) {
    //         cout << temp[i][j] << " ";
    //     }
    //     cout << "\n";
    // }

    cout << temp[N - 1][N - 1] << "\n";
}

static pthread_mutex_t mutexLock;

void* partialCalculation(void* threadId) {
    pthread_mutex_lock(&mutexLock);

    long tId = (long) threadId;
    int srow = (tId / n) * n;  
    int scol = (tId % n) * n;

    int erow = srow + (n - 1); 
    int ecol = scol + (n - 1);

    // cout << "Thread = " << tId << " row(" << srow << ", " << srow + (n - 1) << ") -- col(" << scol << ", " << scol + (n - 1) << ")\n";

    int tArow = (tId / n) * n, tAcol = 0;
    int tBcol = (tId % n) * n, tBrow = 0;

    int K = 0;

    for (int c = 0; c < n; c++) {
        for (int r = tArow, i = srow; r <= tArow + (n - 1); r++, i++) {
            for (int c = tBcol, j = scol; c <= tBcol + (n - 1); c++, j++) {
                for (int k = K; k < n + K; k++) {
                    C[i][j] += A[r][k] * B[k][c];
                }
            }
        }
        K += n;
    }


    // for (int r = tArow, i = srow; r <= tArow + (n - 1); r++, i++) {
    //     for (int c = tBcol, j = scol; c <= tBcol + (n - 1); c++, j++) {
    //         for (int k = 2; k < n + 2; k++) {
    //             C[i][j] += A[r][k] * B[k][c];
    //         }
    //     }
    // }

    pthread_mutex_unlock(&mutexLock);
    pthread_exit(NULL);
}

int main(){ 
    
    //* Initialize Matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = i - j;
            B[i][j] = i + j;
            C[i][j] = 0;
        }
    }

    // int start = get_seconds();

    // for (int i = 0; i < N; i++) {
    //     for (int j = 0; j < N; j++) {
    //         for (int k = 0; k < N; k++) {
    //             D[i][j] += A[i][k] * B[k][j];
    //         }
    //     }
    // }

    // int stop = get_seconds();
    // cout << double (start - stop) / CLOCKS_PER_SEC << "\n";

    pthread_t threads[T];

    int start = get_seconds();

    //* Creating Threads
    for (int t = 0; t < T; t++) {
        int thread = pthread_create(&threads[t], NULL, partialCalculation, (void*)t);
    }

    //* Joining Threads
    for (int t = 0; t < T; t++) {
        void* status;
        int thread = pthread_join(threads[t], &status);
    }

    int stop = get_seconds();
    cout << "Time taken to multiply " << N << " * " << N << " matrix = " << double (stop - start) / CLOCKS_PER_SEC << " secs\n";

    pthread_exit(NULL);
    return 0; 
} 