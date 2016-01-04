#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

#include "generate_soil.h"
#include "my_macro.h"

void
generate_soil( uint8_t *dst[3], int wid, int hgt )
{
    int     row;
    int     col;
    int     component_idx;
    
    // Clear the frames
    for (row = 0; row < hgt; ++row)
    {
       for (col = 0; col < wid; ++col)
       {
            for (component_idx = 0; component_idx < 3; ++component_idx)
            {
                ARR( dst[component_idx], col, row, wid ) = RND_RANGE(0,16);
            }
       }
    }
}
