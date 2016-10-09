#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <malloc.h>

#include "bmp.h"

void
main( int argc, void *argv[] )
{
    uint8_t *pic_buf[3];

    int     wid;
    int     hgt;

    int     i;
    int     idx_v;
    int     idx_h;

    wid = 512;
    hgt = 512;

    // Allocate pic_buf
    for (i = 0; i < 3; i++)
    {
        pic_buf[i] = (uint8_t *) malloc( wid * hgt );
        
        assert(pic_buf[i] != NULL); 
    }

    // Fill in values
    for (idx_v = 0; idx_v < hgt; ++idx_v)
    {
        for (idx_h = 0; idx_h < wid; ++idx_h)
        {
            for (i = 0; i < 3; ++i)
            {
                ARR( pic_buf[i], idx_h, idx_v, wid ) = idx_h & 0xFF;
            }
        }
    }
    bmp_write( "out.bmp", pic_buf, wid, hgt );
}
