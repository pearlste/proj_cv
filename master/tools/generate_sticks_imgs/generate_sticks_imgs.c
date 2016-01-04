#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "bmp.h"
#include "generate_sticks.h"
#include "generate_sticks_frame.h"
#include "generate_weed.h"

int
main( int argc, char **argv )
{
    int     arg_idx;
    
    int     frame_num;
    int     n_frames;
    
    char    out_filename[1024];
    
    int     component_idx;
    
    uint8_t *dst[3];
    uint8_t *leaf[3];

    int     num_frames;
    int     wid;
    int     hgt;
    int     line_wid;
    int     line_hgt;
    int     num_lines;
    int     num_angles;

    int     leaf_wid;
    int     leaf_hgt;

    if (argc != 8)
    {
        fprintf( stderr, "Usage: %s <n_frames> <wid> <hgt> <line_wid> <line_hgt> <num_lines> <num_angles>\n\n", argv[0] );
        exit(1);
    }
        
    arg_idx = 1;
    sscanf( argv[arg_idx++], "%d", &num_frames );
    sscanf( argv[arg_idx++], "%d", &wid );
    sscanf( argv[arg_idx++], "%d", &hgt );
    sscanf( argv[arg_idx++], "%d", &line_wid );
    sscanf( argv[arg_idx++], "%d", &line_hgt );
    sscanf( argv[arg_idx++], "%d", &num_lines );
    sscanf( argv[arg_idx++], "%d", &num_angles );
    
    bmp_read( "leaf_233.bmp", leaf, &leaf_wid, &leaf_hgt );

    srand(0);
        
    for (component_idx = 0; component_idx < 3; ++component_idx)
    {
        dst[component_idx] = malloc(wid * hgt);
    }

    n_frames = 1;
    
    for (frame_num = 0; frame_num < num_frames; ++frame_num)
    {
        generate_soil(dst, wid, hgt);

        generate_grass(dst, wid, hgt, num_angles, line_wid, line_hgt, num_lines * 95/100 );
        
        generate_weed(dst, wid, hgt, leaf, leaf_wid, leaf_hgt, num_angles, 256, 5);

        generate_grass(dst, wid, hgt, num_angles, line_wid, line_hgt, num_lines * 5/100);

        sprintf(out_filename, "out_%05d.bmp", frame_num);
        bmp_write( out_filename, dst, wid, hgt);
        fprintf( stderr, "." );
    }
    printf( "\n\n" );
	return 0;
}
