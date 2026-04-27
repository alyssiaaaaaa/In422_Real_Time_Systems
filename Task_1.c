#include <stdlib.h> // pour le rand()
#include <stdio.h>

int main(void) {
    int a = rand() % 900000 + 100000; // le % 900000 + 100000 permet de générer un nombre aléatoire entre 100000 et 999999 (grand nombre)
    int b = rand() % 900000 + 100000; 
    int product = a * b;
    printf("Product: %d\n", product);

    return 0;
}




    // printf("Enter two numbers: ");
    // scanf("%d %d", &a, &b); // si on veut demander à l'utilisateur de proposer les nombres

