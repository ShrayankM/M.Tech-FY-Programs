#include "mpi.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>


//* 10 Million Numbers
#define N 10000000
#define MAX 10000
int array[N];

void merge(int array[], int L, int M, int H) {
    int* C = (int*)malloc((H - L + 1) * sizeof(int));

    int i = L, j = M + 1;
    int k = 0;
    while (i <= M && j <= H) {
        if (array[i] < array[j]) C[k++] = array[i++];
        else                     C[k++] = array[j++];
    }

    while (i <= M) C[k++] = array[i++];
    while (j <= H) C[k++] = array[j++];

    for (int i = L; i <= H; i++)
        array[i] = C[i - L];
}

void mergesort(int array[], int L, int H) {
    if (L < H) {
        int M = (L + H)/2;
        mergesort(array, L, M);
        mergesort(array, M + 1, H);
        merge(array, L, M, H);
    }
}

void sort_recursive(int array[], int arrSize, int currRank, int maxRank, int rankIndex) {
    MPI_Status status;

    int sharedProcess = currRank + pow(2, rankIndex);
    rankIndex++;

    if (sharedProcess > maxRank) {
        mergesort(array, 0, arrSize - 1);
        return;
    }

    int M = (arrSize - 1)/2;
    MPI_Send((array + M + 1), (arrSize - M - 1), MPI_INT, sharedProcess, M, MPI_COMM_WORLD);
    sort_recursive(array, (M + 1), currRank, maxRank, rankIndex);
    MPI_Recv((array + M + 1), (arrSize - M - 1), MPI_INT, sharedProcess, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

    merge(array, 0, M, arrSize - 1);
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
    
    // printf("Rank Power = %d\n", rankPower);

    if (rank == 0) {
        for (int i = 0; i < N; i++) {
            array[i] = (rand() % (MAX)) + 1;
        }

        sort_recursive(array, N, rank, size - 1, rankPower);
        // printf("OK rank 0\n");
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