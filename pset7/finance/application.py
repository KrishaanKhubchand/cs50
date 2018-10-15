import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # clean values:
    db.execute("DELETE FROM ledger WHERE quantity = :none", none = 0.0)

    #obtain values:
    userData1 = db.execute("SELECT * from users WHERE id = :id", id = session["user_id"])
    userData = userData1[0]
    ledgerData = db.execute("SELECT * from ledger WHERE id = :id", id = session["user_id"])
    if not ledgerData:
        return redirect("/buy")
    # get cash + total of stock wealth, then add:
    userCash = db.execute("SELECT cash from users WHERE id = :id", id = session["user_id"])
    userCash1 = float(userCash[0]["cash"])
    stockWorth = db.execute("SELECT SUM(totalCost) from ledger WHERE id = :id", id = session["user_id"])
    stockWorth1 = float(stockWorth[0]["SUM(totalCost)"])
    netWorth = stockWorth1 + userCash1
    return render_template("index.html", userData = userData, ledgerData = ledgerData, netWorth = netWorth)
    # create arrays of values
#    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        #check stock existence
        stock = request.form.get("symbol")
        quote = lookup(stock)
        if not stock:
            return apology("ffs man, get your symbols correct!")
        
        #check that int is non-zero, +ve:
        firstQ = request.form.get("shares")
        quantity = int(firstQ)
        if quantity < 1:
            return apology("give me a proper amount of shares fam")
            
        #check if they can afford it...
        price = quote["price"]
        purchaseCost = price * quantity
        purchasingPower1 = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        purchasingPower = purchasingPower1[0]["cash"]
        if purchaseCost > purchasingPower:
            return apology("You can't afford this shit.")
        
        #check if the stock is already in table
        stockIn = db.execute("SELECT * FROM ledger WHERE stockSymbol = :symbol", symbol = stock)
        if stockIn:
            oldQ1 = stockIn[0]["quantity"]
            oldQ = int(oldQ1)
            newQ1 = oldQ + quantity
            currentTotal1 = stockIn[0]["totalCost"]
            currentTotal = int(currentTotal1)
            newTotal1 = purchaseCost + currentTotal
            db.execute("UPDATE ledger SET quantity = :newQ, totalCost = :newTotal WHERE stockSymbol = :symbol", newQ = newQ1, newTotal = newTotal1, symbol = stock)
            db.execute("UPDATE users SET cash = :newCash WHERE id = :id", newCash = purchasingPower - purchaseCost, id = session["user_id"])

        elif not stockIn:
            db.execute("INSERT INTO ledger (id, stockSymbol, stockName, pricePerShare, quantity, totalCost) VALUES (:id, :stockSymbol, :stockName, :price, :quantity, :cost)", id = session["user_id"], stockSymbol = stock, stockName = quote["name"], price = quote["price"], quantity = quantity, cost = purchaseCost)
            db.execute("UPDATE users SET cash = :newCash WHERE id = :id", newCash = purchasingPower - purchaseCost, id = session["user_id"])
        
        # record transaction history in new table
        transType = "Bought"
        db.execute("INSERT INTO history (id, transactionType, actionDate, stockName, stockSymbol, sharePrice, quantity, netFlow) VALUES (:id, :transactionType, DateTime('now'), :stockName, :stockSymbol, :sharePrice, :quantity, :netFlow)", id = session["user_id"], transactionType = transType, stockName = quote["name"], stockSymbol = quote["symbol"], sharePrice = quote["price"], quantity = quantity, netFlow = purchaseCost)
        
        
        # render tempalte, but get DATA for load first!
        userData1 = db.execute("SELECT * from users WHERE id = :id", id = session["user_id"])
        userData = userData1[0]
        ledgerData = db.execute("SELECT * from ledger WHERE id = :id", id = session["user_id"])
        return render_template("index.html", userData = userData, ledgerData = ledgerData)
        
    
    if request.method == "GET":
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    historyTable = db.execute("SELECT * from history WHERE id = :id", id = session["user_id"])
    
    return render_template("history.html", historyTable = historyTable)

@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    currentCash1 = db.execute("SELECT cash from users WHERE id = :id", id = session["user_id"])
    currentCash = int(currentCash1[0]["cash"])
    if request.method == "GET":
        return render_template("deposit.html", currentCash = currentCash)
    
    if request.method == "POST":
        moreCash1 = request.form.get("cashInput")
        moreCash = int(moreCash1)
        finalCash = currentCash + moreCash
        db.execute("UPDATE users SET cash = :newCash WHERE id = :id", newCash = finalCash, id = session["user_id"])
        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    
    if request.method == "POST":
        symbol = request.form.get("search")
        # should i check if the symbol is valid?
        quote = lookup(symbol)
        if not quote:
            return apology("yo, give me a proper symbol man!")
        return render_template("quoted.html", name = quote["name"], price = quote["price"], symb = quote["symbol"])
    


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "POST":
        
        # check if username is valid (or is it taken?)
        if not request.form.get("username"):
            return apology("We need a username fam!")
        elif not request.form.get("password"):
            return apology("Enter password brah!")
        elif not request.form.get("confirmation"):
            return apology("Enter password confirmation brah!")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Your passwords don't match, you silly banana!")


        # store password safely:
        hashedPass = generate_password_hash(request.form.get("password"))
    
        #check if Username is already in DB:
        usernameCheck = db.execute("SELECT * FROM users WHERE username = :username",
        username = request.form.get("username"))
    
        if usernameCheck:
            return apology("Username taken!")
    
        # SQL 'add to table' command -- create SQL thing before db.execute tho!
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :theHash)",
        username = request.form.get("username"), theHash = hashedPass)
    
        session["user_id"] = request.form.get("username")
        
        return redirect("/")
    
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    ledgerData = db.execute("SELECT * from ledger WHERE id = :id", id = session["user_id"])
    
    if request.method == "POST":
        #get share sell request quanitity; check if above 0, check if user Q = equivelant
        sellQ1 = request.form.get("shares")
        sellQ = int(sellQ1)
        
        #get share Name
        stockSym = request.form.get("theStock")
        # check that user has those holdings to sell:
        userQ1 = db.execute("SELECT quantity from ledger WHERE stockSymbol = :stock", stock = stockSym)
        userQ = int(userQ1[0]["quantity"])
        
        if sellQ > userQ: 
            return apology("sorry, but this is just not going to work...")
        
        # get details for sale: saleValue (price * q), current holding value... newValue
        newQ = userQ - sellQ
        quote = lookup(stockSym)
        currentPrice = int(quote["price"])
        totalSale = currentPrice * sellQ
        oldHoldings1 = db.execute("SELECT totalCost from ledger where stockSymbol= :stock", stock = stockSym)
        oldHoldings = int(oldHoldings1[0]["totalCost"])
        newHoldings = oldHoldings - totalSale
        
        # append quantity and holdings value 
        db.execute("UPDATE ledger SET quantity = :newQuantity, totalCost = :newTotal WHERE stockSymbol = :stock", newQuantity = newQ, newTotal = newHoldings, stock = stockSym)
        
        #cash update!
        cash1 = db.execute("SELECT cash from users WHERE id = :id", id = session["user_id"])
        cash = int(cash1[0]["cash"])
        theCash = cash + totalSale
        db.execute("UPDATE users SET cash = :newCash WHERE id = :id", newCash = theCash, id = session["user_id"]  )

        # add to history! 
        transType = "Sold"
        db.execute("INSERT INTO history (id, transactionType, actionDate, stockName, stockSymbol, sharePrice, quantity, netFlow) VALUES (:id, :transactionType, DateTime('now'), :stockName, :stockSymbol, :sharePrice, :quantity, :netFlow)", id = session["user_id"], transactionType = transType, stockName = quote["name"], stockSymbol = quote["symbol"], sharePrice = quote["price"], quantity = sellQ, netFlow = totalSale)

        
        
        
        return redirect("/")
        
    
    
    if request.method == "GET":
        return render_template("sell.html", ledgerData = ledgerData)

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
