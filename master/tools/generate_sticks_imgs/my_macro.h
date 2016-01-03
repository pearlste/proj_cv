#ifndef MY_MACRO_H
#define MY_MACRO_H

#define ARR( ptr, x, y, stride )  (*((ptr) + (y) * (stride) + (x)))

#define PI                      (3.1415926535897)
#define ROUND_TO_INT(x)         ( (x) >= 0 ? (int) ((x) + 0.5) : (int) ((x) - 0.5) )
#define IN_RANGE(x, min, max)   ( (x) >= (min) && (x) <= (max) )
#define CLIP(x, min, max)       ( (x) < (min) ? (min) : (x) > (max) ? (max) : (x) )
#define RND_RANGE(min, max)     ( (rand() % (1 + (max) - (min))) + (min) ) 
#endif
