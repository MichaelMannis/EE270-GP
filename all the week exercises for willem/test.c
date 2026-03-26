#include <stdio.h>
#include <stdlib.h>

int main(){
    printf("1");
    int * a = NULL;
    free(a);
    return 0;
}