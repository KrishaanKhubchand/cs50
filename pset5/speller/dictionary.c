// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <string.h>
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <strings.h>

typedef struct linkedList {
    char word[LENGTH + 1];
    struct linkedList *next;
}
list;

list *myDict[26] = { NULL };


struct linkedList* create (string newWord) {  //for creating a newElement that can enter our dictionary hash table.
 //   eprintf("create has been called successfully!\n");
   list *newElement = malloc(sizeof(list));
    if (newElement == NULL) { //check for failure
        printf("fail \n");
    }
//    eprintf("no problems w/creating space for the newElement!\n");
    strcpy(newElement->word, newWord);
    newElement->next = NULL; //nextPointer is null for safe keeping! //try calloc instead of next
//    eprintf("newWord should have been assigned, as well as the element! I hope?\n");
    return newElement;
} 

int hash (string newWord) {
   /*
    int l = strlen(newWord);
    for(int i = 0; i < l; i++) {
        if (isalpha(newWord[i]) == 0) {
            if (newWord[i] != "")
   //         eprintf("fail!\n");
            return -1;
        }
    }
*/
    
    int index;
    if (isupper(newWord[0])) {
        index = newWord[0] - 65;
    } else {
       index = newWord[0] - 97;
    }
    return index;
}


// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // toda
    string theWord = (string) word;
    int wordHash = hash(theWord);
    list *cursor = myDict[wordHash];
    while(cursor != NULL) {
        // check
       int cmp = strcasecmp(word, cursor->word);
       if (cmp == 0) {
           return true;
       }
        cursor = cursor->next;
    }
        return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
   FILE *file = fopen(dictionary, "r"); // open file & CHECK if it's legit!
    if (file == NULL)
    {
    fprintf(stderr, "ah darn");
    }
    
    char tempWord[LENGTH + 1];  // storage for words extracted from dict
 
    while(fscanf(file, "%s", tempWord) != EOF) { //for every word in the file, or so I think..
   //     eprintf("%s first\n", tempWord);
//        // get hashCode for the word
    int numero = hash(tempWord);
    if (numero < 0 || numero > 26) {
        return 1;
    }
    // create new element, based on word: 
    list *newElement = create(tempWord);
   // eprintf("%s\n", newElement->word);
    
   // inserting element
    if (myDict[numero] == NULL) { //at beginning of list if there's nothing there...
    myDict[numero] = newElement;
    } else {
        for (list *temp = myDict[numero]; temp != NULL; temp = temp->next) { //at end of list, if there are elements in the list already!
            if (temp->next == NULL) {
            //    temp->next = malloc(sizeof(list));
                temp->next = newElement;
               break; //should leave for & if looops
            } 
        }
    }
    }

  fclose(file);
  return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    int count = 0;
    for (int i = 0; i < 26; i++) {
        list *cursor = myDict[i];
        while (cursor != NULL) {
            count++;
            cursor = cursor->next;
        }
    }
    return count;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
      for (int i = 0; i < 26; i++) {
      list *cursor = myDict[i];
      while (cursor != NULL) {
          list *temp = cursor;
          cursor = cursor->next;
          free(temp);
      }
      if (i == 25) {
          return true;
      }
  }
  
    return false;
}
