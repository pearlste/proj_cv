#include <stdio.h>
#include <assert.h>

#include "bmp.h"

void
bmp_write( char *filename, uint8_t *pic_buf[3], int wid, int hgt )
{
    BITMAPFILEHEADER file_hdr;
    BITMAPINFOHEADER info_hdr;

    FILE    *fp;

    int     i;
    int     idx_v;
    int     idx_h;
    int     file_stride;

    int     idx_dummy;
    int     n_dummy;

    file_hdr.bfType = 'B' | ('M' << 8);
    file_hdr.bfSize = FH_SIZE + IH_SIZE + ((wid*3+3)/4)*4*hgt;  // Each row of pixels must be an integer number of DWORDs, which are 4 bytes
    file_hdr.bfReserved1 = 0;
    file_hdr.bfReserved2 = 0;
    file_hdr.bfOffBits = FH_SIZE + IH_SIZE;                     // The offset, in bytes, from the beginning of the BITMAPFILEHEADER structure to the bitmap bits.

    info_hdr.biSize             = IH_SIZE;  // The number of bytes required by the structure
    info_hdr.biWidth            = wid;      // The width of the bitmap, in pixels
    info_hdr.biHeight           = hgt;
    info_hdr.biPlanes           = 1;
    info_hdr.biBitCount         = 24;
    info_hdr.biCompression      = BI_RGB;
    info_hdr.biSizeImage        = 0;        // Not used for uncompressed images
    info_hdr.biXPelsPerMeter    = 2834;     // 72 dpi
    info_hdr.biYPelsPerMeter    = 2834;     // 72 dpi
    info_hdr.biClrUsed          = 0;
    info_hdr.biClrImportant     = 0;

    fp = fopen( filename, "wb" );
    assert( fp != NULL );

    fwrite( &file_hdr.bfType         , sizeof(WORD ), 1, fp );
    fwrite( &file_hdr.bfSize         , sizeof(DWORD), 1, fp );
    fwrite( &file_hdr.bfReserved1    , sizeof(WORD ), 1, fp );
    fwrite( &file_hdr.bfReserved2    , sizeof(WORD ), 1, fp );
    fwrite( &file_hdr.bfOffBits      , sizeof(DWORD), 1, fp );

    fwrite( &info_hdr.biSize         , sizeof(DWORD), 1, fp ); 
    fwrite( &info_hdr.biWidth        , sizeof(LONG ), 1, fp ); 
    fwrite( &info_hdr.biHeight       , sizeof(LONG ), 1, fp ); 
    fwrite( &info_hdr.biPlanes       , sizeof(WORD ), 1, fp ); 
    fwrite( &info_hdr.biBitCount     , sizeof(WORD ), 1, fp ); 
    fwrite( &info_hdr.biCompression  , sizeof(DWORD), 1, fp ); 
    fwrite( &info_hdr.biSizeImage    , sizeof(DWORD), 1, fp ); 
    fwrite( &info_hdr.biXPelsPerMeter, sizeof(LONG ), 1, fp ); 
    fwrite( &info_hdr.biYPelsPerMeter, sizeof(LONG ), 1, fp ); 
    fwrite( &info_hdr.biClrUsed      , sizeof(DWORD), 1, fp ); 
    fwrite( &info_hdr.biClrImportant , sizeof(DWORD), 1, fp ); 

    file_stride = (wid * 3 + 3) / 4 * 4;     // wid * 3, rounded up to a multiple of 4 bytes
    n_dummy = file_stride - wid * 3;           // number of dummy bytes needed to pad at the end of each row

    for (idx_v = hgt-1; idx_v >= 0; --idx_v)
    {
        for (idx_h = 0; idx_h < wid; ++idx_h)
        {
            for (i = 0; i < 3; ++i)
            {
                fwrite( &ARR( pic_buf[i], idx_h, idx_v, wid), 1, 1, fp );    // Write one pixel component
            }
        }
        for (idx_dummy = 0; idx_dummy < n_dummy; ++idx_dummy)
        {
            fwrite(&ARR(pic_buf[i], 0, 0, wid), 1, 1, fp);
        }
    }
    fclose( fp );
}
