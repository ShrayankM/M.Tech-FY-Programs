#include <stdio.h>
#include <stdlib.h>

#define N 1000000

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

int main(int argc, char* arv[]) {

    int arr[N];
    int L = 1, H = 10;
    for (int i = 0; i < N; i++) {
        arr[i] = (rand() % (H - L + 1)) + L;
    }

    quicksort(arr, 0, N - 1);

    // for (int i = 0; i < N; i++) 
    //     printf("%d\t", arr[i]);
    // printf("\n");

}