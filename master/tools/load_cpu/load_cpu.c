#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int
main( int argc, char *argv[] )
{
    int iterations;
    int i;
    int j;
    int prod;
    
    sscanf( argv[1], "%d", &iterations );
    
    prod = 1;
    
    for (i = 0; i < iterations; ++i)
    {
        for (j = 0; j < 1000000; ++j)
        {
            prod *= prod;
        }
    }
    
    exit(prod);
}
