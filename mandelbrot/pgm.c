/* Francesco Zamar SM3201464 */
#include <stdio.h>
#include "pgm.h"
#include <sys/mman.h>
#include <stdlib.h>
#include <unistd.h>


immagine apri_immagine(const char *filename, int nrows, int ncols) {


  /*La funzione apri_immagine apre un file immagine specificato da filename, 
  imposta le sue dimensioni e mappa il contenuto del file in memoria. 
  Restituisce una struttura immagine che restituisce il risultato, 
  ovvero un'istanza della struttura immagine */


    immagine risultato;
    risultato.ncols = ncols;
    risultato.nrows = nrows;

    risultato.file = fopen(filename, "w+");
    if (risultato.file == NULL) {
        perror("Impossibile aprire il file");
        exit(EXIT_FAILURE);
    }

    int nfile = fileno(risultato.file);
    risultato.offset = fprintf(risultato.file, "P5\n%d %d\n255\n", risultato.ncols, risultato.nrows);
    if (ftruncate(nfile,nrows*ncols*sizeof(unsigned char) + risultato.offset)== -1){
      exit(-1);
    }
    
    
    risultato.pixels = (unsigned char *)mmap((void *)0, nrows*ncols*sizeof(unsigned char) + risultato.offset, PROT_WRITE,MAP_SHARED, nfile, 0 );
    if (risultato.pixels == MAP_FAILED) {
        perror("Mappatura fallita");
        fclose(risultato.file);
        exit(EXIT_FAILURE);
    }
    
    
    return risultato;
}




void chiudiImmagine(immagine *img) {

  /*Funzione in cui viene chiusa l'immagine.
  La funzione prende in parametro un puntatore a una struttura immagine 
  e chiude il file associato effettuando l'unmapping*/


    if (img->file == NULL) {
      exit(-1);
  }
    munmap(img->pixels,img->nrows*img->ncols*sizeof(unsigned char) + img->offset);
    
    fclose(img->file);
}

