def main():
    # get valid int
    while True:
        height = int(input("Gimme Mario's Height: "))
        if height > 0 or height <24:
            break
    

    currentRow = 0
    while currentRow < height:
        # print spaces for each row:
        startSpaces = 1
        while startSpaces < (height-currentRow):
            print(" ", end="")
            startSpaces += 1
        
        #print hashes for each row:
        hashStart = 0
        while hashStart <= (currentRow + 1):
            print("#", end="")
            hashStart += 1
        print()
        currentRow += 1
        
if __name__ == "__main__":
    main()