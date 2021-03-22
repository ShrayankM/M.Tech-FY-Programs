#include<bits/stdc++.h>
using namespace std;

const int N = 1024;

int A[N][N], B[N][N], C[N][N];

double t[3];

double get_seconds() {
    return (double) clock();
}

void displayResult(int temp[N][N]) {
    for (int j = 0; j < N; j++) {
        for (int i = 0; i < N; i++) {
            cout << temp[i][j] <<" ";
        }
        cout << "\n";
    }

    // cout << temp[0][0] << " -- " << temp[N - 1][N - 1] << "\n";
}

int main() {

    int start, stop, sum_ij, flag = 0;

    //* Initialize Matrices
    start = get_seconds();
    for (int j = 0; j < N; j++) {
        for (int i = 0; i < N; i++) {
            A[i][j] = i - j;
            B[i][j] = i + j;
            // C[i][j] = 0;
        }
    }

    stop = get_seconds();
    t[0] = double (stop - start) / CLOCKS_PER_SEC;


    //* Multiply Matrices
    start = get_seconds();
    for (int j = 0; j < N; j++) {
        for (int k = 0; k < N; k++) {
            int r = B[k][j];
            for (int i = 0; i < N; i++) 
                C[i][j] += A[i][k] * r;
        }
    }

    stop = get_seconds();
    t[1] = double (stop - start) / CLOCKS_PER_SEC;


    start = get_seconds();
    for (int j = 0; j < N; j++) {
        sum_ij = 0;
        for (int k = 0; k < N; k++) {
            int r = B[k][j];
            for (int i = 0; i < N; i++)
                sum_ij += A[i][k] * r;
        }

        int temp = 0;
        for (int i = 0; i < N; i++) temp += C[i][j];
        
        if (temp != sum_ij) { 
            cout << "Error in Multiplication\n"; 
            break;
        }
    }

    stop = get_seconds();
    t[2] = double (stop - start) / CLOCKS_PER_SEC;

    cout << "Matrix Initialization time [" << N << " * " << N << "] Matrix = " << t[0] << "\n";
    cout << "Matrix Multiplication time [" << N << " * " << N << "] Matrix = " << t[1] << "\n";
    cout << "Matrix Correctness time = " << t[2] << "\n";
    cout << "Your code speed up = " << t[2]/t[1] << "x \n"; 

    // displayResult(C);

    return 0;
}