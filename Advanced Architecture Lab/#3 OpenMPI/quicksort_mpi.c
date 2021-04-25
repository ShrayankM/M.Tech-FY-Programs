#include "mpi.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>


//* 10 Million Numbers
#define N 10000000
#define MAX 10000
int array[N];

void swap(int *a, int *b) {
    int temp;
    temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int arr[], int L, int H) {
    int pivot = L;
    int i = L;
    for (int j = L; j <= H; j++) {
        if (arr[pivot] > arr[j]) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[pivot], &arr[i]);
    return i;
}

void quicksort(int arr[], int L, int H) {

    if (L < H) {
        int pivot = partition(arr, L, H);
        quicksort(arr, L, pivot - 1);
        quicksort(arr, pivot + 1, H);
    }   
}

void sort_recursive(int array[], int arrSize, int currRank, int maxRank, int rankIndex) {
    MPI_Status status;

    int sharedProcess = currRank + pow(2, rankIndex);
    rankIndex++;

    if (sharedProcess > maxRank) {
        quicksort(array, 0, arrSize - 1);
        return;
    }

    int pivotIndex = partition(array, 0, arrSize - 1);

    MPI_Send((array + pivotIndex + 1), (arrSize - pivotIndex - 1), MPI_INT, sharedProcess, pivotIndex, MPI_COMM_WORLD);
    sort_recursive(array, (pivotIndex + 1), currRank, maxRank, rankIndex);
    MPI_Recv((array + pivotIndex + 1), (arrSize - pivotIndex - 1), MPI_INT, sharedProcess, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
}

int main(int argc, char* argv[]) {

    int size, rank;
	MPI_Init(&argc, &argv);
    double dtime = MPI_Wtime();

	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

    int rankPower = 0;
    while (pow (2, rankPower) <= rank)
        rankPower++;
    
    if (rank == 0) {

        for (int i = 0; i < N; i++) {
            array[i] = (rand() % (MAX)) + 1;
        }

        sort_recursive(array, N, rank, size - 1, rankPower);

        // for (int i = 0; i < N; i++) 
        //     printf("%d\t", array[i]);
        // printf("\n");

        dtime = MPI_Wtime() - dtime;
        printf("Total time = %f secs\n", dtime);
    }
    else {
		MPI_Status status;
		int subarray_size;
		MPI_Probe(MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
		

		MPI_Get_count(&status, MPI_INT, &subarray_size);
			
		int source_process = status.MPI_SOURCE;
		int *subarray = (int*)malloc(subarray_size * sizeof(int));

		MPI_Recv(subarray, subarray_size, MPI_INT, MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		sort_recursive(subarray, subarray_size, rank, size - 1, rankPower);
		MPI_Send(subarray, subarray_size, MPI_INT, source_process, 0, MPI_COMM_WORLD);
    }
    MPI_Finalize();
    return 0;
}