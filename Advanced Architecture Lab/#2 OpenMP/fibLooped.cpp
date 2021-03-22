#include<bits/stdc++.h>
#include<omp.h>

using namespace std;

int main() {

    omp_set_num_threads(4);
    int N = 10000;
    int fibSeq[N + 1], fibPar[N + 1];

    fibSeq[0] = 0; fibSeq[1] = 1;
    fibPar[0] = 0; fibPar[1] = 1;

    double dtime;

    //* Parallel CODE
    dtime = omp_get_wtime();
    #pragma omp parallel 
    {   
        #pragma omp single
        for (int i = 2; i <= N; i++) {
            fibPar[i] = fibPar[i - 2] + fibPar[i - 1];
        }
    }
    dtime = omp_get_wtime() - dtime;

    cout << "Parallel time = " << dtime << " secs. [" << fibPar[N] <<"]" << endl;
    // cout << fibPar[N] << endl;

    //* Sequential CODE
    dtime = omp_get_wtime();
    for (int i = 2; i <= N; i++) {
            fibSeq[i] = fibSeq[i - 2] + fibSeq[i - 1];
    }
    dtime = omp_get_wtime() - dtime;

    cout << "Sequential time = " << dtime << " secs. [" << fibPar[N] << "]" << endl;
    // cout << fibSeq[N] << endl;

    return 0;
}