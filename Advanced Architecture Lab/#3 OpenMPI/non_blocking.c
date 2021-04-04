#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <mpi.h>

const int MESSAGE_SIZE = 100;

MPI_Request request;
MPI_Status  status;
int request_complete = 0;

int main(int argc, char ** argv) {

    char message[MESSAGE_SIZE];

    int processes, id;
    MPI_Init(&argc, &argv);

    MPI_Comm_size(MPI_COMM_WORLD, &processes);
    MPI_Comm_rank(MPI_COMM_WORLD, &id);

    if (id == 0) {
        int i;
        for (i = 0; i < 10; i++) {
            printf("Process(0) executing iteration %d\n", i);
            if (i % 2 == 0) {
                sprintf(message, "Message from process(0) to process (1) CNT = %d", i);
                sleep(2);
                printf("Working for 4 seconds. P(0)\n");
                // MPI_Send(message, strlen(message)+1, MPI_CHAR, 1, i, MPI_COMM_WORLD);
                MPI_Isend(message, strlen(message)+1, MPI_CHAR, 1, i, MPI_COMM_WORLD, &request);
                sleep(2);

                if (!request_complete)
                    MPI_Test(&request, &request_complete, &status);
                
                if (!request_complete)
                    MPI_Wait(&request, &status);
            }
        }
    }
    else {
        // for (int j = 0; j < 5; j++)
        //     printf("Process(1) executing iteration %d\n", j);
        for (int i = 0; i < 10; i++) {
            if (i % 2 == 0) {
               sleep(1);
            //    MPI_Recv(message, MESSAGE_SIZE, MPI_CHAR, 0, i, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
               MPI_Irecv(message, MESSAGE_SIZE, MPI_CHAR, 0, i, MPI_COMM_WORLD, &request);
               MPI_Wait(&request, &status);
               printf("%s \n", message); 
               sleep(1);
               printf("Working for 2 second. P(1)\n");
            }
        }
    }

    MPI_Finalize();
    return 0;
}