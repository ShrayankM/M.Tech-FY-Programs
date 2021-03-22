#include<bits/stdc++.h>
#include<omp.h>
using namespace std;

#define THREAD 32

int main() {

    int n = 1E8;

    double sum = 0.0, factor = 1.0;
    double dtime;

    dtime = omp_get_wtime();
    for (int i = 0; i < n; i++) {
        factor = (i % 2 == 0) ?  1.0 : -1.0; 
        sum += factor/(2 * i + 1);
    }
    dtime = omp_get_wtime() - dtime;
    cout << "PI Approx = " << 4.0 * sum << " Time = " << dtime << " secs. [SEQUENTIAL]" << endl;

    sum = 0.0;

    dtime = omp_get_wtime();
    #pragma omp parallel for num_threads(THREAD) reduction(+:sum) private(factor)
    for (int i = 0; i < n; i++) {
        factor = (i % 2 == 0) ?  1.0 : -1.0; 
        sum += factor/(2 * i + 1);
    }
    dtime = omp_get_wtime() - dtime;
    cout << "PI Approx = " << 4.0 * sum << " Time = " << dtime << " secs. [PARALLEL]" << endl;
    return 0;
}