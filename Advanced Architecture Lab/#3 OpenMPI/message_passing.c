#include <stdio.h>
#include <string.h>
#include <mpi.h>

const int MESSAGE_SIZE = 100;

int main(int argc, char ** argv) {

    char message[MESSAGE_SIZE];

    int processes, id;
    MPI_Init(&argc, &argv);

    MPI_Comm_size(MPI_COMM_WORLD, &processes);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);

    if (id != 0) {
        sprintf(message, "Message from process(%d) to process (0)", id);
        MPI_Send(message, strlen(message)+1, MPI_CHAR, 0, 0, MPI_COMM_WORLD);
    }
    else {
        for (int p = 1; p < processes; p++) {
            MPI_Recv(message, MESSAGE_SIZE, MPI_CHAR, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            printf("%s \n", message);
        }
    }

    MPI_Finalize();
    return 0;
}