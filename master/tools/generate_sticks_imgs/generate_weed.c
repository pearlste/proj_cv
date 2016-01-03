#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "rotate_and_offset.h"
#include "my_macro.h"

#define RENDER_FRACTION (4)

#define FP_SHIFT (8)
#define FP_ROUND (1 << (FP_SHIFT-1))

#define RED_MIN (110)
#define RED_MAX (130)
#define GRN_MIN (190)
#define GRN_MAX (210)
#define BLU_MIN (60)
#define BLU_MAX (70)
#define LUM_MAX (300)
#define LUM_MIN (100)

#define LEAF_SZ_MUL_MIN ((int) (0.125 * 256))
#define LEAF_SZ_MUL_MAX ((int) (1.000 * 256))

#define COLOR_MUL_MIN   ((int) (0.95 * 256))
#define COLOR_MUL_MAX   ((int) (1.1 * 256))

void
generate_sticks_frame( uint8_t *dst[3], int wid, int hgt, int *leaf[3], int leaf_wid, int leaf_hgt, int num_angles, int leaf_scale, int num_leaves )
{
    int     leaf_idx;
    
    int     row;
    int     col;
    int     frac_hor;
    int     frac_ver;
    
    int     component_idx;
    
    double  angle;
    double  x;
    double  y;
    double  rx;
    double  ry;
    
    int     irx;
    int     iry;
    
    int     offset_x;
    int     offset_y;
    
    int     line_wid;
    int     line_hgt;
    
    int     lum;
    int     color[3];

    int     scale_factor;  // U7.8
    
    int     leaf_radius;
    
    leaf_radius = (MAX(leaf_wid, leaf_hgt) * leaf_scale + FP_ROUND) >> FP_SHIFT;
    
    offset_x = RND_RANGE( leaf_radius, wid - leaf_radius );
    offset_y = RND_RANGE( leaf_radius, hgt - leaf_radius );
    
    for ( leaf_idx = 0; leaf_idx < num_leaves; ++leaf_idx )
    {
        angle    = ((double) (rand() % num_angles)) * 2.0 * PI / num_angles;    // between 0 and 2PI
        
        // Step 1: Rotate four vertices
        // Step 
        for (row = 0; row <= leaf_hgt; ++row)
        {
            for (frac_ver = 0; frac_ver < RENDER_FRACTION; ++frac_ver)
            {
                y = ((double) row) + 1.0/RENDER_FRACTION * frac_ver;
                        
                for (col = -line_wid/2; col <= line_wid/2; ++col)
                {
                    for (frac_hor = 0; frac_hor < RENDER_FRACTION; ++frac_hor)
                    {
                        int y_eff;
                        
                        x = ((double) col) + 1.0/RENDER_FRACTION * frac_hor;
                        
                        rotate_and_offset(x, y_eff, angle, offset_x, offset_y, &rx, &ry);
                        
                        irx = ROUND_TO_INT(rx);
                        iry = ROUND_TO_INT(ry);
                        
                        //printf( "irx=%4d, iry=%4d\n", irx, iry );
                        
                        if ( IN_RANGE( irx, 0, wid-1 ) && IN_RANGE( iry, 0, hgt-1 ) )
                        {
                            for (component_idx = 0; component_idx < 3; ++component_idx)
                            {
                                ARR(dst[component_idx], irx, iry, wid) = CLIP(color[component_idx], 0, 255);
                            }
                        }
                    }
                }
            }
        }
    }
}
