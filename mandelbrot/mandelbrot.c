/* Francesco Zamar SM3201464 */
#include <stdio.h>
#include <complex.h>
#include <math.h>
#include "mandelbrot.h"

int complexMandelbrot(float complex complesso, int max_iter)
{   

    /*La funzione calcola se un numero appartiene o non appartiene all'insieme di Mandelbrot.
    Vengono presi in input: un numero complesso e le iterazioni massime.
    La funzione ritorna: -  i , ovvero il numero di iterazioni che sono servite per far uscire il numero dall'insieme di Mandelbrot.
                         - -1 se l'iterazione non ha superato il raggio il numero appartiene all'insieme di Mandelbrot. */

                         
    float raggio = 2.0;
    float complex serieZn = 0;
    for(int i=0; i < max_iter ;i++){

        serieZn = (serieZn * serieZn) + complesso;
        
        if (cabs(serieZn)>=raggio){

            return i;
        }


    }

    return -1;

}