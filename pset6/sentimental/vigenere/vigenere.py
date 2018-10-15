import sys

def main():
    if len(sys.argv) != 2:
        print("nah fam!")
        sys.exit(1)
    

    theKey = sys.argv[1]
    keyLength = len(theKey)
    
    if theKey.isalpha() == False:
        print("invalid input")
        sys.exit(1)
        
    
    plainText = input("plainText: ") #getText
    keyIndex = 0  #createIndexForKey
  #  print(f"{theKey[keyIndex]}")
    
    forDisplay = "ciphertext: "

    for letter in plainText:
        toCheck = theKey[keyIndex % keyLength]
        if toCheck.islower() == True:
            theNumber = 97
        elif toCheck.isupper() == True:
            theNumber = 65
        
        shift = ord(theKey[keyIndex % keyLength]) - theNumber
        if letter.islower() == True:
            newLetterNumber = ((((ord(letter) - 97)+ shift) % 26) + 97)
            newLetterChar = chr(newLetterNumber)
            forDisplay += newLetterChar
            keyIndex += 1
        elif letter.isupper() == True:
            newLetterNumber = ((((ord(letter) - 65)+ shift) % 26) + 65)
            newLetterChar = chr(newLetterNumber)
            forDisplay += newLetterChar
            keyIndex +=1
        else:
            newLetterChar = letter
            forDisplay += newLetterChar
    
    print(forDisplay)

if __name__ == "__main__":
    main()