#ifndef BMP_HDR_H
#define BMP_HDR_H

#include <stdint.h>
#include <Windows.h>

#if 0
typedef uint8_t  BYTE;
typedef uint16_t WORD;
typedef uint32_t DWORD;
typedef uint32_t LONG;
#endif

#define FH_SIZE ( \
    sizeof(WORD ) + \
    sizeof(DWORD) + \
    sizeof(WORD ) + \
    sizeof(WORD ) + \
    sizeof(DWORD) )

#define IH_SIZE ( \
    sizeof(DWORD) + \
    sizeof(LONG ) + \
    sizeof(LONG ) + \
    sizeof(WORD ) + \
    sizeof(WORD ) + \
    sizeof(DWORD) + \
    sizeof(DWORD) + \
    sizeof(LONG ) + \
    sizeof(LONG ) + \
    sizeof(DWORD) + \
    sizeof(DWORD) )

#if 0
typedef struct tagBITMAPFILEHEADER {
    WORD  bfType;
    DWORD bfSize;
    WORD  bfReserved1;
    WORD  bfReserved2;
    DWORD bfOffBits;
} BITMAPFILEHEADER, *PBITMAPFILEHEADER;

typedef struct tagBITMAPINFOHEADER {
    DWORD biSize;
    LONG  biWidth;
    LONG  biHeight;
    WORD  biPlanes;
    WORD  biBitCount;
    DWORD biCompression;
    DWORD biSizeImage;
    LONG  biXPelsPerMeter;
    LONG  biYPelsPerMeter;
    DWORD biClrUsed;
    DWORD biClrImportant;
} BITMAPINFOHEADER, *PBITMAPINFOHEADER;

typedef struct tagRGBQUAD {
    BYTE rgbBlue;
    BYTE rgbGreen;
    BYTE rgbRed;
    BYTE rgbReserved;
} RGBQUAD;
#endif
#endif