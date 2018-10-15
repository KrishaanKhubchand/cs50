def main():
    while True:
        try:
            dollarChange = float(input("How much change do I owe you, in dollars? "))
        except ValueError:
            print("sorry, that ain't a real number fam")
            continue
        else:
            change = int(dollarChange * 100)
            if change > 0:
                break
    
    coinAmount = 0
    
    while change > 25 or change == 25:
        coinAmount = coinAmount + 1
        change = change - 25
    
    while change >= 10:
        coinAmount += 1
        change -= 10
    
    while change >= 5:
        coinAmount += 1
        change -= 5
    
    while change >=1:
        coinAmount += 1
        change -= 1
    
    
    print(f"{coinAmount}")

    
if __name__ == "__main__":
    main()