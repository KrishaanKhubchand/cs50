#include <stdio.h>
#include <cs50.h>
#include <stdio.h> 
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]) {
    
    if (argc != 2) {
        printf("Come on cuh!\n");
        return 1;
    }
    string llaves = argv[1];
    int keyLength = strlen(llaves);
    
    for (int i = 0; i < keyLength; i++) {
        if (isalpha(llaves[i])){

        } else {
            printf("failed\n");
            return 1;
        }
    }
    
    string plainText = get_string("paintext: "); 
    int plainTextLength = strlen(plainText);
    string cipherText = malloc(plainTextLength * sizeof(char));
    int keyIndex = 0;
    for (int index = 0; index < plainTextLength; index++) {
        if isupper(llaves[keyIndex % keyLength]) {
        int shift = llaves[keyIndex % keyLength] - 65;
        if (isupper(plainText[index])) {
            cipherText[index] = ((((plainText[index] - 65) + shift) % 26) + 65);
            keyIndex++;
        } else if (islower(plainText[index])) {
            cipherText[index] = ((((plainText[index] - 97) + shift) % 26) + 97);
            keyIndex++;
        } else {
        cipherText[index] = plainText[index];
        } }  
    
     else if islower(llaves[keyIndex % keyLength]) {
        int shift = llaves[keyIndex % keyLength] - 97;
        if isupper(plainText[index]) {
            cipherText[index] = ((((plainText[index] - 65) + shift) % 26) + 65);
            keyIndex++;
        } else if (islower(plainText[index])) {
            cipherText[index] = ((((plainText[index] - 97) + shift) % 26) + 97);
            keyIndex++;
        }
        else {
        cipherText[index] = plainText[index];
        }
    }
    
    else {
        cipherText[index] = plainText[index];
    }
    
 }
    printf("ciphertext: %s\n", cipherText);
}