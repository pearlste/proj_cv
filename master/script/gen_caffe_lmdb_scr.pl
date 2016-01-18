#!/usr/bin/perl

# Usage: gen_caffe_lmdb_scr.pl <jpg_path>

use strict;
use warnings;
use File::Path;
use File::Copy;
use File::Spec::Functions;

my $jpg_path;
my $dir_handle;
my $file_list;

my $the_file;
my @the_files;

my $file_num;
my @file_nums;

my $num_files;

my $i;
my $category;

    if (@ARGV != 1)
    {
        die "Usage: gen_caffe_lmdb_scr.pl <jpg_path>\n\n";
    }
    
    $jpg_path = $ARGV[0];
    
    opendir $dir_handle, $jpg_path or die "Cannot open directory: $!";
    my @file_list = readdir $dir_handle;
    closedir $dir_handle;

    foreach $the_file (@file_list)
    {
        $the_file =~ /[a-zA-Z\.\-_]*([0-9]+).jpg/;
        
        $file_num = $1;
        
        if ( $file_num )
        {
            #printf( "$1\n" );
            push @the_files, $the_file;
        }
        
    }

    @the_files = sort {$a cmp $b} @the_files;
    
    $num_files = $#the_files + 1;
    
    for ($i = 0; $i < $num_files; ++$i)
    {
        if ($i < $num_files/2)
        {
            printf( "$the_files[$i] 1\n" );
        }
        else
        {
            printf( "$the_files[$i] 0\n" );
        }
    }
    