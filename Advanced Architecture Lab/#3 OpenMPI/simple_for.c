#include <mpi.h>
#include <stdio.h>

int main(int argc, char ** argv) {

    int processes, id;
    MPI_Init(&argc, &argv);

    MPI_Comm_size(MPI_COMM_WORLD, &processes);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);


    for (int i = 0; i < 3; i++) {
        printf("Process %d of %d Running [Index = %d]\n", id, processes, i);
    }

    MPI_Finalize();
}