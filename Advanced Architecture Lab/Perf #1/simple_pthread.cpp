#include<bits/stdc++.h> 
#include<pthread.h>
#include<time.h>

using namespace std; 

const int N = 1024;
const int n = 32;

const int T = (N * N)/(n * n);

double getSecondsCpu() {
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

    cout << temp[0][0] << " -- " << temp[N - 1][N - 1] << "\n";
}

static pthread_mutex_t mutexLock;

void* partialCalculation(void* threadId) {
    // pthread_mutex_lock(&mutexLock);

    long tId = (long) threadId;
    int srow = (tId / (N/n)) * n;  
    int scol = (tId % (N/n)) * n;

    int erow = srow + (n - 1); 
    int ecol = scol + (n - 1);

    // cout << "Thread = " << tId << " row(" << srow << ", " << srow + (n - 1) << ") -- col(" << scol << ", " << scol + (n - 1) << ")\n";

    int tArow = (tId / (N/n)) * n, tAcol = 0;
    int tBcol = (tId % (N/n)) * n, tBrow = 0;

    int K = 0;

    for (int c = 0; c < (N/n); c++) {
        for (int r = tArow, i = srow; r <= tArow + (n - 1); r++, i++) {
            for (int c = tBcol, j = scol; c <= tBcol + (n - 1); c++, j++) {
                for (int k = K; k < n + K; k++) {
                    C[i][j] += A[r][k] * B[k][c];
                }
            }
        }
        K += n;
    }

    // pthread_mutex_unlock(&mutexLock);
    pthread_exit(NULL);
}

int main(){ 
    
    //* Initialize Matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = i - j;
            B[i][j] = i + j;
            C[i][j] = 0;
            D[i][j] = 0;
        }
    }

    int start, stop;
    time_t begin, end;

    start = getSecondsCpu();
    time(&begin);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                D[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    stop = getSecondsCpu();
    time(&end);

    cout << "TILE SIZE = " << n << "\n";

    cout << "(CPU  SECS) Time taken to multiply " << N << " * " << N << " matrix (NORMAL) = " << double (stop - start) / CLOCKS_PER_SEC << " secs\n";
    cout << "(WALL SECS) Time taken to multiply " << N << " * " << N << " matrix (NORMAL) = " << (end - begin) << " secs\n";

    cout << "=============================================================================\n";

    pthread_t threads[T];

    start = getSecondsCpu();
    time(&begin);

    //* Threads 
    for (int t = 0; t < T; t++) {
        int thread = pthread_create(&threads[t], NULL, partialCalculation, (void*)t);
    }

    //* Joining Threads
    for (int t = 0; t < T; t++) {
        void* status;
        int thread = pthread_join(threads[t], &status);
    }

    stop = getSecondsCpu();
    time(&end);
    cout << "(CPU  SECS) Time taken to multiply " << N << " * " << N << " matrix (THREAD) = " << double (stop - start) / CLOCKS_PER_SEC << " secs\n";
    cout << "(WALL SECS) Time taken to multiply " << N << " * " << N << " matrix (THREAD) = " << (end - begin) << " secs\n";

    cout << "=============================================================================\n";

    displayMatrix(C);
    // // cout << "\n";
    displayMatrix(D);

    pthread_exit(NULL);
    return 0; 
} 

//* jackson@ubuntu:~/GitHub/M.Tech-FY-Programs/Advanced Architecture Lab/Perf #1$ ./thread
//? TILE SIZE = 64
//? (CPU  SECS) Time taken to multiply 2048 * 2048 matrix (NORMAL) = 280.027 secs
//? (WALL SECS) Time taken to multiply 2048 * 2048 matrix (NORMAL) = 280 secs
//? =============================================================================
//? (CPU  SECS) Time taken to multiply 2048 * 2048 matrix (THREAD) = 136.777 secs
//? (WALL SECS) Time taken to multiply 2048 * 2048 matrix (THREAD) = 36 secs
//? =============================================================================
//? 1433752576 -- 1425366016
//? 1433752576 -- 1425366016
//* jackson@ubuntu:~/GitHub/M.Tech-FY-Programs/Advanced Architecture Lab/Perf #1$ g++-8 -o thread simple_pthread.cpp -lpthread
//? simple_pthread.cpp: In function ‘int main()’:
//? simple_pthread.cpp:106:83: warning: cast to pointer from integer of different size [-Wint-to-pointer-cast]
//?          int thread = pthread_create(&threads[t], NULL, partialCalculation, (void*)t);
//?                                                                                    ^
//* jackson@ubuntu:~/GitHub/M.Tech-FY-Programs/Advanced Architecture Lab/Perf #1$ ./thread
//? TILE SIZE = 32
//? (CPU  SECS) Time taken to multiply 2048 * 2048 matrix (NORMAL) = 282.544 secs
//? (WALL SECS) Time taken to multiply 2048 * 2048 matrix (NORMAL) = 282 secs
//? =============================================================================
//? (CPU  SECS) Time taken to multiply 2048 * 2048 matrix (THREAD) = 105.46 secs
//? (WALL SECS) Time taken to multiply 2048 * 2048 matrix (THREAD) = 27 secs
//? =============================================================================
//? 1433752576 -- 1425366016
//? 1433752576 -- 1425366016
