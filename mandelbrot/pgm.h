/* Francesco Zamar SM3201464 */
#ifndef PGM_H
#define PGM_H

struct __attribute__ ((packed)) _immagine{

    FILE *file;
    int nrows;
    int ncols;
    unsigned char *pixels;
    int offset;
};
typedef struct _immagine immagine;

immagine apri_immagine(const char *filename, int nrows, int ncols);

void chiudiImmagine(immagine *img);

#endif