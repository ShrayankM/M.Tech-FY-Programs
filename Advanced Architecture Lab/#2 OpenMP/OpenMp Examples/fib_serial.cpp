#include<bits/stdc++.h>
#include<omp.h>
using namespace std;

// #define N int(1E5)
#define THREAD 8


int main() {

    int n = 20;
    double dtime;
    int fib[n];

    fib[0] = 0; fib[1] = 1;


    dtime = omp_get_wtime();
    #pragma omp parallel shared(n, fib) 
    {
        #pragma omp parallel for
        for (int i = 2; i < n; i++) {
            fib[i] = fib[i - 1] + fib[i - 2];
        }
    }
    dtime = omp_get_wtime() - dtime;

    cout << "time = " << dtime << " secs.\n"; 

    // #pragma omp parallel for shared(n, fib)
    // for (int i = 2; i < n; i++) {
    //     fib[i] = fib[i - 1] + fib[i - 2];
    // }


    for (int i = 0; i < n; i++)
        cout << fib[i] << " ";
    cout << "\n";
    return 0;
}