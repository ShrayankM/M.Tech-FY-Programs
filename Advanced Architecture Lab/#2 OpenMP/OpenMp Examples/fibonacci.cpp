#include<bits/stdc++.h>
#include<omp.h>
using namespace std;

#define N int(1E5)
#define THREAD 4

bool memo[N];
long fibStore[N];

long fib(int n, int type) {
    if (n < 2) {
        memo[n] = true;
        fibStore[n] = n;
        return n;
    }

    if (memo[n] == true) return fibStore[n];

    long a, b;

    if (type == 1) {
        #pragma omp task shared(a)
        a = fib(n - 1, type);

        #pragma omp task shared(b)
        b = fib(n - 2, type);

        #pragma omp taskwait
        {
            memo[n] = true;
            fibStore[n] = a + b;
            return a + b;
        }
    }
    a = fib(n - 1, type);
    b = fib(n - 2, type);
    memo[n] = true;
    fibStore[n] = a + b;
    return a + b;
}

int main() {

    cout << "Threads = " << THREAD << endl;
    int n = int(90);
    double dtime;

    dtime = omp_get_wtime();
    cout << "Fib(" << n << ") = " << fib(n, 0) << endl;
    dtime = omp_get_wtime() - dtime;

    cout << "SEQUENTIAL TIME = " << dtime << " secs." << endl << "\n";

    omp_set_num_threads(THREAD);

    dtime = omp_get_wtime();
    #pragma omp parallel 
    {
        #pragma omp single
        cout << "Fib(" << n << ") = " << fib(n, 1) << endl;
    }
    dtime = omp_get_wtime() - dtime;
    cout << "PARALLEL TIME = " << dtime << " secs." << endl;
    return 0;
}