#include <math.h>

#include "rotate_and_offset.h"

void
rotate_and_offset(
    double  x, 
    double  y, 
    double  angle,
    int     offset_x, 
    int     offset_y,
    double  *rx,
    double  *ry)
{
    double cos_t;
    double sin_t;
    
    cos_t = cos(angle);
    sin_t = sin(angle);
    
// |-  -|    |-              -| |- -|
// | dx | =  | cos(t) -sin(t) | | x |
// | dy |    | sin(t)  cos(t) | | y |
// |-  -|    |-              -| |- -|
    
    *rx = cos_t * x - sin_t * y + offset_x;
    *ry = sin_t * x + cos_t * y + offset_y;
}
