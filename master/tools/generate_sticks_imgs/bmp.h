#ifndef BMP_H
#define BMP_H

#include "bmp_hdr.h"
#include "my_macro.h"

void
bmp_write(char *filename, uint8_t *pic_buf[3], int wid, int hgt);

void
bmp_read_hdr(char *filename, uint8_t *pic_buf[3], int *wid, int *hgt);

void
bmp_read(char *filename, uint8_t *pic_buf[3], int *wid, int *hgt);

#endif
