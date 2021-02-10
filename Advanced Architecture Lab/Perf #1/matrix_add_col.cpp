#include<bits/stdc++.h> 
using namespace std; 

const int N = 1024;
int A[N][N], B[N][N], C[N][N];

double t[3];

double get_seconds() {
    return (double) clock();
}

int main(){ 

    int start, stop, sum_ij, flag = 0;

    //* Initialize Matrices
    start = get_seconds();
    for (int j = 0; j < N; j++) {
        for (int i = 0; i < N; i++) {
            A[i][j] = i - j;
            B[i][j] = i + j;
        }
    }

    stop = get_seconds();
    t[0] = double (stop - start) / CLOCKS_PER_SEC;

    //* Add Matrices
    start = get_seconds();
    for (int j = 0; j < N; j++) {
        for (int i = 0; i < N; i++) {
            C[i][j] = A[i][j] + B[i][j];
        }
    }

    stop = get_seconds();
    t[1] = double (stop - start) / CLOCKS_PER_SEC;

    //* Check Correctness of Addition
    start = get_seconds();
    for (int j = 0; j < N; j++) {
        for (int i = 0; i < N; i++) {
            sum_ij = A[i][j] + B[i][j];

            if (sum_ij != C[i][j]) {
                cout << "Error in addition \n";
                flag = 1;
                break;
            }

            if (flag) break;
        }
    }

    stop = get_seconds();
    t[2] = double (stop - start) / CLOCKS_PER_SEC;

    // cout << t[0] << " - " << t[1] << " - " << t[2] << "\n";

    cout << "Matrix Initialization time = " << t[0] << "\n";
    cout << "Matrix Addition time = " << t[1] << "\n";
    cout << "Matrix Correctness time = " << t[2] << "\n";
    cout << "Your code speed up = " << t[2]/t[1] << "x \n";  
    return 0; 
} 