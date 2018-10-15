// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // get scaleFactor
    char *tempFactor = argv[1];
    int scaleFactor = atoi(tempFactor);
    
    if (scaleFactor < 0 || scaleFactor > 100) {
        fprintf(stderr, "Usage: give proper number\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    
  // create output's header info and file, to be scaled...
    BITMAPFILEHEADER newBF = bf;
    BITMAPINFOHEADER newBI = bi;
    
    printf("%i and %i", bf.bfSize, newBF.bfSize);
  // scaling the width/height: 
    newBI.biWidth *= scaleFactor;
    newBI.biHeight *= scaleFactor;

    // new padding
    int newPadding = (4 - (newBI.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    // new imageSize etc.
    newBI.biSizeImage = (((sizeof(RGBTRIPLE) * newBI.biWidth) + newPadding) * abs(newBI.biHeight));
    newBF.bfSize = newBI.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
       printf("%i and %i", bf.bfSize, newBF.bfSize);
    // write outfile's BITMAPFILEHEADER
    fwrite(&newBF, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&newBI, sizeof(BITMAPINFOHEADER), 1, outptr);

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

// an experiment: 
    // for each row aka iterating over infile's scanlines: 
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++) {
        
        // for SF - 1 times:
        for (int m = 0; m < scaleFactor - 1; m++) {
                 
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++) {
            
            // temporary storage ->
            RGBTRIPLE triple;
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            // do this for every scale factor unit... 
         for (int k = 0; k < scaleFactor; k++) {
            // write RGB triple to outfile -- tested with SF as quantity
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
         }
        }
        
        int negWidth = -bi.biWidth * sizeof(RGBTRIPLE);
        
              fseek(inptr, negWidth, SEEK_CUR);
              
         for (int k = 0; k < newPadding; k++) // i think this adds padding! 
        {
            fputc(0x00, outptr);
        }  
        // fseek -> from current position, back by width, reg input...
  
        }
    // out of loop: also, store and write x SF for each pixel, PLUS Padding && skip input padding via fseek; find this set to be dodgy
                // iterate over pixels in scanline
       for (int j = 0; j < bi.biWidth; j++) {
            
            
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            // do this for every scale factor unit... 
         for (int k = 0; k < scaleFactor; k++) {
            // write RGB triple to outfile -- tested with SF as quantity
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
         }
        } 
        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);

        // then add it back (to demonstrate how)
       for (int k = 0; k < newPadding; k++)
        {
            fputc(0x00, outptr);
        } 
        
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
