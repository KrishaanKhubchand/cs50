# Questions

## What's `stdint.h`?

A library that enables programmes to use differently sized (width-wise) Int types, such as uint32_t and uint8_t. 


## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

This enables efficient cyclying of calculations and minimises dealings with remainders.
You also gain different degrees of precision which can be tremendously helpful. 8 bit ints, for example, are great for representing RGB hexes.


## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE = 1 Byte = 8 bits.
DWORD = 4 Bytes = 32 bits. 
LONG = 4 Bytes = 32 bits.
WORD = 2 Bytes = 16 bits.

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

First 2 bytes of a BMP are a WORD type, called BFType. In hex: 0x4D42. In decimal: 19778. In chars: BM.

## What's the difference between `bfSize` and `biSize`?

biSize refers to the number of bytes required by the structure (acc image). bfSize refers to the number of bytes required by the acc file.

## What does it mean if `biHeight` is negative?

The image is top-down, with the bottom at the top. Origin is upper left corner. Must compress via BI RGB or BI BITFIELDS.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

biBitCount

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If there's no file to point to.

## Why is the third argument to `fread` always `1` in our code?

We're dealing with just one file, of BITMAP File Header size.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

0.

## What does `fseek` do?

It is searching for the pixel information inbetween the padding.

## What is `SEEK_CUR`?

Helps move file pointer forward based on search/addition.