#include <stdio.h>
#include <complex.h>
#include <stdlib.h>
#include <omp.h>
#include <sys/mman.h>
#include <math.h>
#include "pgm.h"
#include "mandelbrot.h"



int main(int argc, char **argv) {

    // Gestione degli argomenti da linea di comando
    if(argc != 4){
        printf("Uso: %s <path> <max_iter> <nrows>\n", argv[0]);
        return -1;
    }

    int max_iter = atoi(argv[2]);
    if(max_iter<1){
        printf("Il numero delle iterazioni dev'essere maggiore di 1");
        return -1;
    }
    int nrows = atoi(argv[3]);
    if(nrows<1 || nrows%2 != 0){
        printf("Il numero delle righe dev'essere maggiore di 1 e divisibiule per 2");
        return -1;
    }


    int ncols = 1.5*nrows;

    immagine img = apri_immagine(argv[1], nrows, ncols);
0
    /*Calcolo la suddivisione in pixels del piano*/
                                                                                 //   k = (2 ncols + 3)   ->   i = k/ncols= (2 ncols + 3)/ ncols = 2 con resto di 3
#pragma omp parallel for collapse(2)    // ncols = 200  nrows = 6
    for (int i = 0; i < nrows; i++) { // for 0 <= k < ncols*nrows  se k < ncols                    ncols <= k < 2 * ncols   k = ncols * 2  .....  k = ncols * nrows -1
        for (int j = 0; j < ncols; j++) { // i = (int) k / ncols        i = 0                       i = 1                   i = 2          -----  i = nrows - 1
            float real = -2.0 + j * 3.0 / (ncols-1); // j = k % ncols   j = 0, 1, ..., ncols-1      j = 0, ..., ncols -1    j = 0          .....  j = ncols - 1
            float imag = -1.0 + i * 2.0 / (nrows-1);
            float complex c = real + imag * I;                                                                                             //  k = i * cols + j
                                                                                                                                            //  k = nrows* ncols + ( - ncols + ncols) - 1
            unsigned char color;
            int n = complexMandelbrot(c,max_iter);
            if(n== -1){
                color = (unsigned char) 255;
            }else{
                color=(unsigned char)((255*log(n))/log(max_iter));
            }
            
            img.pixels[i * ncols + j + img.offset] = color;

        }
    }

    chiudiImmagine(&img);

    return 0;
}




