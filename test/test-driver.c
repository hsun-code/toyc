#include <stdio.h>

extern int fib(int num);
extern int bubble_sort(int arr[], int len);

void main()
{
    // how to check the result.
    int result = fib(20);
    printf("fib result is %d\n", result);

    int arr[10] = {3, 5, 1, -7, 4, 9, -6, 8, 10, 4};
    result = bubble_sort(arr, 10);
    int inx;
    for (inx = 0; inx < 10; inx++)
        printf("%d", arr[inx]);
}
