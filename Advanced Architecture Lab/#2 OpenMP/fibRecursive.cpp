#include<bits/stdc++.h>
#include<omp.h>

using namespace std;

const int N = 1E6;

int fibPar[N], fibSeq[N];
bool memoPar[N], memoSeq[N];

int calculateFibPar(int n) {
    if (n < 2) {
        memoPar[n] = true;
        fibPar[n] = n;
        return n;
    }

    if (memoPar[n] == true) return fibPar[n];

    int a, b;
    #pragma omp task shared(a) firstprivate(n)
    a = calculateFibPar(n - 1);

    #pragma omp task shared(b) firstprivate(n)
    b = calculateFibPar(n - 2);

    #pragma omp taskwait
    fibPar[n] = a + b;

    memoPar[n] = true;
    return fibPar[n];
}

int calculateFibSeq(int n) {
    if (n < 2) {
        memoSeq[n] = true;
        fibSeq[n] = n;
        return fibSeq[n];
    }

    if (memoSeq[n] == true) return fibSeq[n];

    memoSeq[n] = true;
    fibSeq[n] = calculateFibSeq(n - 1) + calculateFibSeq(n - 2);
    return fibSeq[n];
}

int main() {
    
    int n = 10000;
    double dtime;

    omp_set_num_threads(4);

    dtime = omp_get_wtime();
    #pragma omp parallel shared(n) 
    {
        #pragma omp single
        calculateFibPar(n + 1);
    }
    dtime = omp_get_wtime() - dtime;

    cout << "Parallel time = " << dtime << " secs. [" << fibPar[n] <<"]" << endl;

    dtime = omp_get_wtime();
    calculateFibSeq(n + 1);
    dtime = omp_get_wtime() - dtime;

    // for (int i = 0; i < n; i++) 
    //     cout << fibSeq[i] << "\t";
    // cout << "\n";

    cout << "Sequential time = " << dtime << " secs. [" << fibSeq[n] << "]" << endl;
}