#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>

#define MAIN 0
#define ROWS 1024
#define COLS 1024
#define MAIN_TAG 1
#define WORKER_TAG 2

double A[ROWS][COLS], B[COLS][ROWS], C[ROWS][ROWS];

int main(int argc, char *argv[]) {

    int tasks, id, workers, avgrows, extrarows, offset, tag, rows;


    MPI_Init(&argc, &argv);
    double dtime = MPI_Wtime();
    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &tasks);

    workers = tasks - 1;

    //* Main Thread Works
    if (id == MAIN) {
        printf("Intializing the matrices\n");
        for (int i = 0; i < ROWS; i++) {
            for (int j = 0; j < COLS; j++) {
                A[i][j] = i + j;
            }
        }

        for (int i = 0; i < COLS; i++) {
            for (int j = 0; j < ROWS; j++) {
                B[i][j] = i - j;
            }
        }

        //* Sending Data to Workers
        avgrows = ROWS/workers;
        extrarows = ROWS%workers;
        offset = 0;
        tag = MAIN_TAG;

        for (int w = 1; w <= workers; w++) {
            rows = (w <= extrarows) ? avgrows + 1 : avgrows;

            MPI_Send(&offset, 1, MPI_INT, w, tag, MPI_COMM_WORLD);
            MPI_Send(&rows, 1, MPI_INT, w, tag, MPI_COMM_WORLD);
            MPI_Send(&A[offset][0], rows*COLS, MPI_DOUBLE, w, tag, MPI_COMM_WORLD);
            MPI_Send(&B, COLS*ROWS, MPI_DOUBLE, w, tag, MPI_COMM_WORLD);
            offset = offset + rows;
        }

        tag = WORKER_TAG;
        for (int w = 1; w <= workers; w++) {
            MPI_Recv(&offset, 1, MPI_INT, w, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Recv(&rows, 1, MPI_INT, w, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            MPI_Recv(&C[offset][0], rows*ROWS, MPI_DOUBLE, w, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }

        // for (int i = 0; i < ROWS; i++) {
        //     for (int j = 0; j < ROWS; j++) {
        //         printf("%6.2f   ", C[i][j]);
        //     }
        //     printf("\n");
        // }
    }
    else{
        tag = MAIN_TAG;
        MPI_Recv(&offset, 1, MPI_INT, MAIN, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(&rows, 1, MPI_INT, MAIN, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(&A, rows*COLS, MPI_DOUBLE, MAIN, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        MPI_Recv(&B, COLS*ROWS, MPI_DOUBLE, MAIN, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < COLS; j++) {
                C[i][j] = 0.0;
                for (int k = 0; k < COLS; k++) 
                    C[i][j] += A[i][k] * B[k][j];
            }
        }

        // for (int k = 0; k < COLS; k++) {
        //     for (int i = 0; i < rows; i++)
        //     {
        //         C[i][k] = 0.0;
        //         for (int j = 0; j < COLS; j++)
        //             C[i][k] = C[i][k] + A[i][j] * B[j][k];
        //     }
        // }

        tag = WORKER_TAG;
        MPI_Send(&offset, 1, MPI_INT, MAIN, tag, MPI_COMM_WORLD);
        MPI_Send(&rows, 1, MPI_INT, MAIN, tag, MPI_COMM_WORLD);
        MPI_Send(&C, rows*ROWS, MPI_DOUBLE, MAIN, tag, MPI_COMM_WORLD);
    }

    if (id == 0) {
        dtime = MPI_Wtime() - dtime;
        printf("Id = %d Time = %f secs\n", id, dtime);
    }
    MPI_Finalize();
}