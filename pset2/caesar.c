#include <stdio.h>
#include <cs50.h>
#include <stdio.h> 
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[]) {
    
    // check arg count
    if (argc != 2) {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    
    // make key int
    string number = argv[1];
    int key = atoi(number);
    
    // check if key is valid
    
    if (key <= 0) {
        printf("Usage: ./caesar k \n");
        return 1;
    }
    
    string plainText = get_string("plaintext: ");
    int textLength = strlen(plainText);
    string newWord = malloc(textLength * sizeof(char));
    for(int index = 0; index < textLength; index++) {
        if (isalpha(plainText[index])) {
            if (isupper(plainText[index])) {
                newWord[index] = ((((plainText[index] - 65) + key) % 26) + 65);
            } else if (islower(plainText[index])) {
                newWord[index] = ((((plainText[index] - 97) + key) % 26) + 97);
            } else {
                newWord[index] = plainText[index];
            }
        }
        else {
            newWord[index] = plainText[index];
        }
    }
    printf("ciphertext: %s\n", newWord);

}