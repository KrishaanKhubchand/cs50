def main():
    file = open("twofile", "r")
    word = file.read()
    print(word)
    length = len(file)
    length2 = len(word)
    print(length)
    print(length2)

if __name__ == "__main__":
    main()