#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "bmp.h"
#include "generate_sticks.h"
#include "generate_sticks_frame.h"
#include "generate_weed.h"      
#include "generate_soil.h"
#include "generate_grass.h"

#define NUM_ANGLES (1 << 15)

int
main( int argc, char **argv )
{
    int     arg_idx;
    
    int     frame_num;
    
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
    int     num_weed_leaves;
    
    char    dst_dir[1024];
    char    which_weeds_str[1024];
    char    cmd_str[1024];

    int     weed_frames;
    
    int     leaf_wid;
    int     leaf_hgt;

    if (argc != 10)
    {
        fprintf( stderr, "\n" );
        fprintf( stderr, "Usage: %s <n_frames> <wid> <hgt> <line_wid> <line_hgt> <num_lines> <num_weed_leaves> <dst_dir> < ALL | NONE | HALF >\n\n", argv[0] );
        fprintf( stderr, "NOTE:  ALL  = all frames have weed leaves\n" );
        fprintf( stderr, "       NONE = no frames have weed leaves\n" );
        fprintf( stderr, "       HALF = first half of all frames have weed leaves\n\n" );
        exit(1);
    }
        
    arg_idx = 1;
    sscanf( argv[arg_idx++], "%d", &num_frames );
    sscanf( argv[arg_idx++], "%d", &wid );
    sscanf( argv[arg_idx++], "%d", &hgt );
    sscanf( argv[arg_idx++], "%d", &line_wid );
    sscanf( argv[arg_idx++], "%d", &line_hgt );
    sscanf( argv[arg_idx++], "%d", &num_lines );
    sscanf( argv[arg_idx++], "%d", &num_weed_leaves );

    strcpy( dst_dir,         argv[arg_idx++] );
    strcpy( which_weeds_str, argv[arg_idx++] );

    if      (strcmp( which_weeds_str, "ALL")  == 0)     weed_frames = num_frames;
    else if (strcmp( which_weeds_str, "NONE") == 0)     weed_frames = 0;
    else if (strcmp( which_weeds_str, "HALF") == 0)     weed_frames = num_frames/2;
    else
    {
        fprintf( stderr, "\n" );
        fprintf( stderr, "NOTE:  ALL  = all frames have weed leaves\n" );
        fprintf( stderr, "       NONE = no frames have weed leaves\n" );
        fprintf( stderr, "       HALF = first half of all frames have weed leaves\n\n" );
        exit(1);
    }

    sprintf( cmd_str, "mkdir -p %s", dst_dir );
    fprintf( stderr, "\n%s\n", cmd_str );
    system( cmd_str );
                    
    bmp_read( "leaf_233.bmp", leaf, &leaf_wid, &leaf_hgt );
    fprintf( stderr, "\nRead weed leaf\n" );
    
    fprintf( stderr, "\n" );
    fprintf( stderr, "num_frames        = %d\n", num_frames     );
    fprintf( stderr, "wid               = %d\n", wid            );
    fprintf( stderr, "hgt               = %d\n", hgt            );
    fprintf( stderr, "line_wid          = %d\n", line_wid       );
    fprintf( stderr, "line_hgt          = %d\n", line_hgt       );
    fprintf( stderr, "num_lines         = %d\n", num_lines      );
    fprintf( stderr, "num_weed_leaves   = %d\n", num_weed_leaves);
    fprintf( stderr, "\n" );

    srand(0);
        
    for (component_idx = 0; component_idx < 3; ++component_idx)
    {
        dst[component_idx] = malloc(wid * hgt);
    }

    for (frame_num = 0; frame_num < num_frames; ++frame_num)
    {
        generate_soil(dst, wid, hgt);

        generate_grass(dst, wid, hgt, NUM_ANGLES, line_wid, line_hgt, num_lines * 95/100 );
        
        if (frame_num < weed_frames)
        {
            generate_weed(dst, wid, hgt, leaf, leaf_wid, leaf_hgt, NUM_ANGLES, 256, num_weed_leaves);
        }
        
        generate_grass(dst, wid, hgt, NUM_ANGLES, line_wid, line_hgt, num_lines * 5/100);

        fprintf( stderr, "." );
        sprintf(out_filename, "%s/out_%05d.bmp", dst_dir, frame_num);
        bmp_write( out_filename, dst, wid, hgt);
        fprintf( stderr, "." );
    }
    printf( "\n\n" );
	return 0;
}
