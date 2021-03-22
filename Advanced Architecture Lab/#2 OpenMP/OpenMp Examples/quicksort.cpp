#include<bits/stdc++.h>
#include<omp.h>

using namespace std;

#define N int(1E5)
#define MAX_NUM 20

void displayArr(int A[]) {
    for (int i = 0; i < N; i++) 
        cout << A[i] << "\t";
    cout << "\n";
}

int partition(int A[], int L, int H) {
    int pivot = A[L];
    int i = L;

    for (int j = L + 1; j <= H; j++) {
        if (A[j] <= pivot){
            i = i + 1;
            swap(A[i], A[j]);
        }
    }
    swap(A[i], A[L]);
    return i;
}

//* type = 0 (Sequential), type = 1 (Parallel)
void quicksort(int A[], int L, int H, int type) {
    if (L < H) {
        int pivotPos = partition(A, L, H);

        if (type == 1 && (L + (pivotPos - 1)) > 1000) {
            #pragma omp task
            {
                quicksort(A, L, pivotPos - 1, type);
                // cout << "THREAD ID = " << omp_get_thread_num() << " [" << L << ", " << pivotPos - 1 << "]" << endl;
            } 
            
            #pragma omp task
            {
                quicksort(A, pivotPos + 1, H, type);
                // cout << "THREAD ID = " << omp_get_thread_num() << " [" << pivotPos + 1 << ", " << H << "]" << endl;
            }
            return;
        } 
        quicksort(A, L, pivotPos - 1, type);
        quicksort(A, pivotPos + 1, H, type);
              
    }
}

int main() {
    
    srand((unsigned) time(0));
    int arr[N];
    double dtime;

    for (int i = 0; i < N; i++) {
        arr[i] = (rand() % MAX_NUM) + 1;
    }

    dtime = omp_get_wtime();
    quicksort(arr, 0, N - 1, 0);
    dtime = omp_get_wtime() - dtime;
    cout << "SEQUENTIAL TIME = " << dtime << " secs." << endl;
    // displayArr(arr);

    omp_set_num_threads(4);
    for (int i = 0; i < N; i++) {
        arr[i] = (rand() % MAX_NUM) + 1;
    }

    dtime = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp single 
        quicksort(arr, 0, N - 1, 1);
    }
    dtime = omp_get_wtime() - dtime;

    cout << "PARALLEL TIME = " << dtime << " secs." << endl;
    // displayArr(arr);
    return 0;
}

