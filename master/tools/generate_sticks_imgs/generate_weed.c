#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

#include "generate_weed.h"
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

typedef struct
{
    int x;
    int y;
} vertex_t;

void
generate_weed(uint8_t *dst[3], int wid, int hgt, uint8_t *leaf[3], int leaf_wid, int leaf_hgt, int num_angles, int leaf_scale, int num_leaves)
{
    int     leaf_idx;

    int     row;
    int     col;

    int     component_idx;

    double  angle;
    double  rx;
    double  ry;

    int     irx;
    int     iry;

    int     offset_x;
    int     offset_y;

    int     leaf_radius;

    vertex_t    top_lft;
    vertex_t    bot_lft;
    vertex_t    top_rgt;
    vertex_t    bot_rgt;

    int         color_offset[3];

    leaf_radius = MAX(leaf_wid, leaf_hgt);

    offset_x = RND_RANGE(leaf_radius, wid - leaf_radius);
    offset_y = RND_RANGE(leaf_radius, hgt - leaf_radius);

    // Assume that the leaf is oriented vertically, and that it's origin is at x=leaf_wid/2, y=0

    for (component_idx = 0; component_idx < 3; ++component_idx)
    {
        color_offset[component_idx] = RND_RANGE(0, 10) - 5;
    }

    for (leaf_idx = 0; leaf_idx < num_leaves; ++leaf_idx)
    {
        int     lft;
        int     rgt;
        int     top;
        int     bot;

        double  x;
        double  y;

        angle = ((double)(rand() % num_angles)) * 2.0 * PI / num_angles;    // between 0 and 2PI
        //angle = 0.0;
        // Step 1: Rotate four vertices of the leaf image, and translate origin
        // Step 2: Find bounding box that includes the rotated vertices (min/max x, min/max y)
        // Step 3: Scan bounding box, rotate each pixel by negative angle.  If inside leaf img
        //         get pixel value.  If not BG pixel, then render it.

        // top_lft @ (-leaf_wid/2, leaf_hgt );
        // bot_lft @ (-leaf_wid/2, 0        );
        // top_rgt @ ( leaf_wid/2, leaf_hgt );
        // bot_rgt @ ( leaf_wid/2, 0        );

        rotate_and_offset(-leaf_wid / 2.0, (double)leaf_hgt, angle, 0, 0, &x, &y); top_lft.x = ROUND_TO_INT(x); top_lft.y = ROUND_TO_INT(y);
        rotate_and_offset(-leaf_wid / 2.0, 0.0,              angle, 0, 0, &x, &y); bot_lft.x = ROUND_TO_INT(x); bot_lft.y = ROUND_TO_INT(y);
        rotate_and_offset(leaf_wid / 2.0,  (double)leaf_hgt, angle, 0, 0, &x, &y); top_rgt.x = ROUND_TO_INT(x); top_rgt.y = ROUND_TO_INT(y);
        rotate_and_offset(leaf_wid / 2.0,  0.0,              angle, 0, 0, &x, &y); bot_rgt.x = ROUND_TO_INT(x); bot_rgt.y = ROUND_TO_INT(y);

        // Bounding box of rotated rectangle
        lft = MIN(MIN(top_lft.x, top_rgt.x), MIN(bot_lft.x, bot_rgt.x));
        rgt = MAX(MAX(top_lft.x, top_rgt.x), MAX(bot_lft.x, bot_rgt.x));
        top = MIN(MIN(top_lft.y, top_rgt.y), MIN(bot_lft.y, bot_rgt.y));
        bot = MAX(MAX(top_lft.y, top_rgt.y), MAX(bot_lft.y, bot_rgt.y));

        for (row = top; row <= bot; ++row)
        {
            int transl_x;
            int transl_y;

            transl_y = row + offset_y;

            for (col = lft; col <= rgt; ++col)
            {
                rotate_and_offset(col, row, -angle, 0, 0, &rx, &ry);

                irx = ROUND_TO_INT(rx) + leaf_wid/2;
                iry = leaf_hgt - 1 - ROUND_TO_INT(ry);

                transl_x = col + offset_x;

                // Ensure that rotated pixel is in leaf rectangle
                // and that the translated rotated point is in dst rectangle
                if (IN_RANGE(irx, 0, leaf_wid - 1) &&
                    IN_RANGE(iry, 0, leaf_hgt - 1) &&
                    IN_RANGE(transl_x, 0, wid - 1) &&
                    IN_RANGE(transl_y, 0, hgt - 1) &&
                    (ARR(leaf[0], irx, iry, leaf_wid) + ARR(leaf[1], irx, iry, leaf_wid) + ARR(leaf[1], irx, iry, leaf_wid)))
                {
                    int alpha;
                    // Alpha blend based on sum of RGB, with 100% at sum = 64
                    alpha = ARR(leaf[0], irx, iry, leaf_wid) + ARR(leaf[1], irx, iry, leaf_wid) + ARR(leaf[2], irx, iry, leaf_wid);
                    alpha = CLIP(alpha, 0, 256);
                    
                    for (component_idx = 0; component_idx < 3; ++component_idx)
                    {
                        ARR(dst[component_idx], transl_x, transl_y, wid) = CLIP(
                            (alpha * (ARR(leaf[component_idx], irx, iry, leaf_wid) + color_offset[component_idx]) +
                            (256 - alpha)*ARR(dst[component_idx], transl_x, transl_y, wid) + 64) >> 8, 0, 255);
                    }
                }
            }
        }
    }
}
