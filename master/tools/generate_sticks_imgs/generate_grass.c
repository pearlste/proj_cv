#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "generate_grass.h"
#include "rotate_and_offset.h"
#include "my_macro.h"

#define RENDER_FRACTION (4)

#define FP_SHIFT (8)
#define FP_ROUND (1 << (FP_SHIFT-1))

#define RED_MIN (130-10)
#define RED_MAX (130+10)
#define GRN_MIN (164-15)
#define GRN_MAX (164+15)
#define BLU_MIN (96-7)
#define BLU_MAX (96+7)
#define LUM_MAX (300)
#define LUM_MIN (100)

#define LINE_SZ_MUL_MIN ((int) (0.125 * 256))
#define LINE_SZ_MUL_MAX ((int) (1.000 * 256))

#define COLOR_MUL_MIN   ((int) (0.95 * 256))
#define COLOR_MUL_MAX   ((int) (1.1 * 256))

typedef struct
{
    int offset_x;
    int offset_y;
    int color;
    int angle;
    int num_angles;
    int line_wid;
    int line_hgt;
} blade_info;

void
generate_grass( uint8_t *dst[3], int wid, int hgt, int num_angles, int _line_wid, int _line_hgt, int num_lines )
{
    int     line_idx;
    
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
    
    for ( line_idx = 0; line_idx < num_lines; ++line_idx )
    {
        angle    = ((double) (rand() % num_angles)) * PI / num_angles;    // between 0 and PI
        offset_x = (rand() % wid);
        offset_y = (rand() % hgt);
        
        scale_factor = RND_RANGE(LINE_SZ_MUL_MIN, LINE_SZ_MUL_MAX);
        line_wid = (_line_wid * scale_factor + FP_ROUND) >> FP_SHIFT;
        
        scale_factor = RND_RANGE(LINE_SZ_MUL_MIN, LINE_SZ_MUL_MAX);
        line_hgt = (_line_hgt * scale_factor + FP_ROUND) >> FP_SHIFT;
        
        //angle = 1;
        //offset_x = offset_y = 200;
        
        lum      = RND_RANGE(LUM_MIN, LUM_MAX);
        color[0] = (lum * RND_RANGE(BLU_MIN, BLU_MAX) + FP_ROUND) >> FP_SHIFT;  // red component
        color[1] = (lum * RND_RANGE(GRN_MIN, GRN_MAX) + FP_ROUND) >> FP_SHIFT;  // grn component
        color[2] = (lum * RND_RANGE(RED_MIN, RED_MAX) + FP_ROUND) >> FP_SHIFT;  // blue component

        // Go through each pixel in the rectangle, in increments of 1/2 pixel, and color in based on rotation and offset
        // Keep track of the index of the highest numbered line, and color, that passes through the center pixel
        
        // Think of the grass being horizontal
        
        for (row = -line_hgt/2; row <= line_hgt/2; ++row)
        {
            scale_factor = RND_RANGE(COLOR_MUL_MIN, COLOR_MUL_MAX);
            
            for (component_idx = 0; component_idx < 3; ++component_idx)
            {
                color[component_idx] = ((color[component_idx] * scale_factor) + FP_ROUND) >> FP_SHIFT;
            }
            
            for (frac_ver = 0; frac_ver < RENDER_FRACTION; ++frac_ver)
            {
                y = ((double) row) + 1.0/RENDER_FRACTION * frac_ver;
                        
                for (col = -line_wid/2; col <= line_wid/2; ++col)
                {
                    for (frac_hor = 0; frac_hor < RENDER_FRACTION; ++frac_hor)
                    {
                        int y_eff;
                        
                        x = ((double) col) + 1.0/RENDER_FRACTION * frac_hor;
                        
                        // Need to scale y as a function of x
                        // y_eff = y * (1 - exp(x/tau))
                        // Let tau = line_wid
                        
                        y_eff = (int) (y * (1.0 - exp( (-0.25 * (col+line_wid/2)) / line_hgt )) + 0.5);
                        
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
