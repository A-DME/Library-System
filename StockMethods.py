# get stocked books in a list
def getstock():
    """This method is for getting the stocked books in the library file in 
the form of a list of dictionaries with keys of the books identifiers so that each
dictionary on itself is a book."""
    bfile= open('stock.txt','r') # books.txt**

    keys= bfile.readline().strip().split('|')
    values= bfile.readlines()
    bfile.close()
    for i in range(len(values)):
        values[i]= values[i].strip().split('|')

    stock=list(dict(zip(keys,value)) for value in values)

    return stock


# function to get pretty values
def prettyVals(lstofbooks):
    """Based on keys and values of the books, this function returns standard lengths for the 
area that each column takes to make a nice tabular form"""
    prettyList=[]
    # getting a list of keys for the comparisons done below
    keys=[*lstofbooks[0].keys()] # the zero here is because some times this method gets a list of only one book
    for key in keys:
        standard=0 # initializing a standard value for the column area
        for book in lstofbooks:
            if len(book[key]) > standard: 
                # if the value of the current value is bigger then we assign it as standard
                # unless length of key is bigger so the standard shoud be the length of the key
                standard= len(book[key]) if len(book[key])>len(key) else len(key)+2
        prettyList.append(standard) # and finally putting the column's standard
    
    # For price column, the prices should appear with two dicimal digits 
    # and since most prices are below a thousand, then there would be 6 spaces
    # required for the column's area, and for making it prettier we add 2 more spaces so the total is 8
    prettyList[-1]=8 

    return prettyList

# function to make prettier Line
def prettierLine(Linelst,prettyList,totalprice):
    """Taking a list containing a record values along with the pretty standards, this function presents a
nicely printed table record/line.
*NOTE*: It also takes a boolean value that indicates whether table should contain the total price column or not."""
    # apart from Title and Author columns(left justified), the column values are centered 
    for i in range(len(Linelst)):
        Linelst[i]=' '+Linelst[i].ljust(prettyList[i]) if i in [1,2] else Linelst[i].center(prettyList[i]) 

    if Linelst[-1].strip().isnumeric(): # Case book line
        Linelst[-1]=('%.2f'%float(Linelst[-1])).center(prettyList[-1]) # making the price appear with two dicimal digits
        if totalprice: # case total price required
            Linelst.append(' '+'%.2f'%(float(Linelst[-1])*int(Linelst[-4]))+' QR') #adding total price of copies
    else: # Case key line
        if totalprice: # case total price required
            Linelst.append(' Totally') # adding the column header for the total price
    
    line= '|'.join(Linelst)+'\n' # forming the pretty line
    return line 

# function to convert list of books to list of lines
def books2lines(lstofbooks,prettyMode,totalprice):
    """The aim here is to turn a list of dictionaries (books) into a list of lines with either for displaying
in a nicely formed table (if the pretty mode is on) or for just writing it back to the file.

*NOTE*: The total price is also decided to be added or not."""
    
    linlst=[] # initializing the list of lines
    
   # case pretty mode ON (for displaying a nice tabular format)
    if prettyMode:
        standards=prettyVals(lstofbooks) # getting the standards
        linlst.append(prettierLine([*lstofbooks[0].keys()],standards,totalprice)) # table header
        for book in lstofbooks: # turning every book(dic) in the list into a pretty line
            linlst.append(prettierLine([*book.values()],standards,totalprice)) # adding a pretty line of book
   
   # case pretty mode OFF (for writing back into file)
    else:
        linlst.append('|'.join([*lstofbooks[0].keys()])+'\n') # header
        for book in lstofbooks: # turning every book(dic) in the list into a line
            linlst.append('|'.join([*book.values()])+'\n') # adding a line of book

    return linlst 


# function to update the stock file 
def updatefile(stock):
    """This function re-writes the stock into the file to keep it up to date"""
    lines=books2lines(stock,False,False) # preparing the lines to be written into the file
    updatedfile= open('file.txt','w') # openning the file in write mode
    updatedfile.writelines(lines) # writing the lines of the updated stock
    updatedfile.close() # closing the file

# function to add book to the stock 
def add_book(stock):
    """This function aims to add a book, by taking its information of it from the user, to a list of
dictionaries (books)."""
    
    book={} # intializing the book record
    # taking book credintials from user:
   
    # easy/short way
    # keys = [*stock[0].keys()]
    # for key in keys: 
    #     book[key]=input(f"Enter {key}: ")
    
    # hard way ...better in a way
    # (in the future might put some restrictions on copies, year, price as being numbers
    # and as a valid year for a book)
    book['ISBN']=input('Enter the ISBN: ')
    book['Title']=input('Enter the title: ')
    book['Author']=input('Enter the author: ')
    book['Copies']=input('Enter the number of copies: ')
    book['Year']=input('Enter the year: ')
    book['Publisher']=input('Enter the publisher name: ')
    book['Price']=input('Enter the price: ')

    stock.append(book) # adding the book to the list of books
    updatefile(stock) # updating the library
    print('.....Record added.') # a confirmation message


# function to update book in the stock 
def update_book(stock):
    """The purpose of this function is to find a book by its stock code and add or remove copies of it."""
    
    code=input('Enter the ISBN of the book: ').strip() # getting stock code from user
    
    for book in stock:# searching for the book by given code
        if book['ISBN'] == code: # if found
            copies = int(book['Copies']) 
            print(f"Book: {book['Title']}, Copies: {copies}") # displaying book's name and available copies
            print('1-add copies\n2-remove copies')
            choice=input('What do you want to do?: ') # acquiring a choice from the user
            
            if choice.strip().lower() in ['1','a','add']: # case addition
                while True:
                    try:
                        # acquiring a number of copies from the user
                        ad=int(input('Enter number of copies to be removed: ').strip())
                    except:# if the user enters an invalid input for the operation
                        print("Please enter a number not a text!")
                        continue
                    if ad >= 0 : # case positive input
                        book['Copies']=str(copies+ad)
                        print('.....Record updated successfully.')
                        break
                    else: # case negative iput.. asking user if they want to remove copies
                        print(f'Adding a negative number of copies is considered removing.\nWould you like to remove {-ad} copies?')
                        print('1-Yes\n2-No')
                        achoice= input('Your choice: ')
                        if achoice.lower().strip() in ['1','y','yes']: # case user agrees to remove copies
                            if -ad < copies: # case available amount of copies
                                book['Copies']=str(copies+ad)
                                print('.....Record updated successfully.')
                                break
                            else: # case no sufficient copies, cancel operation
                                print("Sorry, can't remove more copies than the available ones. Operation cancelled!")
                                break
                        elif achoice.lower().strip() in ['2','n','no']:# case user refuses to remove copies
                            print('Do you want to try again?') # offering another chance of updating
                            print('1-Yes\n2-No')
                            answer= input('Your choice: ')
                            if answer.lower() in ['1','y','yes']: # case taking chance
                                continue
                            else: # case denying
                                print('Operation cancelled!')
                                break
                        else: # case invalid choice, cancel operation
                            print('Invalid choice. Operation cancelled!')
                            break            
            elif choice.strip().lower() in ['2','r','remove']: # case removal
                while True:
                    try:
                        # acquiring number of copies from user
                        re=int(input('Enter number of copies to be removed: '))
                    except:# if the user enters an invalid input for the operation
                        print("Please enter a number not a text!")
                        continue
                    if re < copies: # case available copies 
                        if re >= 0: # case positive input
                            book['Copies']=str(copies-re)
                            print('.....Record updated successfully.')
                            break
                        else: # case negative input, asking user if they wanna add copies
                            print(f"Subtracting a negative number is considered addition.\nWould you like to add {-re} copies?")
                            print('1-Yes\n2-No')
                            rchoice= input('Your choice: ')
                            if rchoice.lower().strip() in ['1','y','yes']: # if user agrees, then add the copies
                                book['Copies']=str(copies-re)
                                print('.....Record updated successfully.')
                                break
                            elif rchoice.lower().strip() in ['2','n','no']: # case user refuses, offer another try
                                print('Do you want to try again?')
                                print('1-Yes\n2-No')
                                answer= input('Your choice: ')
                                if answer.lower().strip() in ['1','y','yes']: # case take
                                    continue
                                else: # case refuse/invalid choice
                                    print('Operation cancelled!')
                                    break
                    else: # case no sufficient copies, offer another try
                        print('Cannot remove more than the stored copies.')
                        print('Do you want to try again?')
                        print('1-Yes\n2-No')
                        answer= input('Your choice: ')
                        if answer.lower() in ['1','y','yes']: # case take
                            continue
                        else: # case refuse/invalid choice
                            print('Operation cancelled!')
                            break
            else: # case invalid choice (add/remove)
                print('Invalid choice.\nOperation cancelled!')
            break

    else: # case book not found
        print('No book in the stock with the given ISBN')
    updatefile(stock)


# function to delete book from the stock 
def delete_book(stock):
    """The aim of this function is to remove a book from a list of books if the book exists in it."""
    
    code=input('Enter the ISBN of the book: ') # acquiring book's stock code from user
    for book in stock: # searching for the book in the list of books
        if book['ISBN'] == code: # if book found
            stock.pop(stock.index(book)) # remove it
            print('.....Record deleted.') # confirming message
            break
    else: # case book not found
        print('No book in the stock with the given ISBN')
    updatefile(stock)


# Search by ISBN 
def findByCode(lstofbooks):
    """This function displays all the details of a book, if found, searched by its stock code."""
    isbn=input("Enter the ISBN: ") # acquiring stock code from user
    for book in lstofbooks: # searching in the list of books
        if book['ISBN'] == isbn.strip(): # if book found
            print('Book found\n-----------')
            print('',*books2lines([book],True,False)) # display in a nice way
            break
    else: # case book not found
        print("No book in the stock with the provided ISBN")


# Find books by Publisher name 
def booksByPublisher(lstofbooks):
    """Finds and prints books that are published by a given publisher."""
    wantedBooks=[]
    publisher=input("Enter Publisher name: ") # acquiring publisher name/part of it from user
    for book in lstofbooks: # searching for the wanted books
        if book['Publisher'].lower().find(publisher.strip().lower()) != -1:
            wantedBooks.append(book) # if a book matches, we add it
    # finally we display those books. And if no matchings found a disclaiming message is shown
    print('',*books2lines(wantedBooks,True,False)) if len(wantedBooks)>0 else print('No books found by provided publisher')


# Find books by Author name 
def booksByAuthor(lstofbooks):
    """Finds and prints books that are written by a given author."""
    wantedBooks=[]
    author=input("Enter Author name: ") # acquiring author name/part of it from user
    for book in lstofbooks:# searching for wanted books
        if book['Author'].lower().find(author.strip().lower()) != -1:
            wantedBooks.append(book) # if a book matches, we add it
    # finally we display those books. And if no matchings found a disclaiming message is shown
    print('',*books2lines(wantedBooks,True,False)) if len(wantedBooks)>0 else print('No books found by provided author')

# Calculates verage price
def calcAvg(lstofbooks):
    """Calculates/returns the average price of books in a list."""
    lstofprices= []
    for book in lstofbooks:
        lstofprices.append(float(book['Price'])) # gathering prices into a list
    # then calculating the average by summing the prices over the number of books. Then rounding
    # the result to the nearest two decimal digits
    avg= round(sum(lstofprices)/len(lstofprices),2)
    return avg

# List Books Greater than average price 
def listAboveAvg(lstofbooks):
    """Lists the books above average price."""
    wantedbooks=[] # initializing list of above average price books
    average=calcAvg(lstofbooks) # getting average price
    for book in lstofbooks: 
        if float(book['Price'])>average: # storing a book above average price
            wantedbooks.append(book)
    # finally listing these books
    print('',*books2lines(wantedbooks,True,False))


# Stock Statistics... 
def expandche(lstofbooks):
    """Finds the most and least expensive books."""
    high,low=0,200 # a starting price points just for the sake of the comparison
    for book in lstofbooks:
        if float(book['Price']) > high: # finding the most expensive
            exp=book
        if float(book['Price']) < low: # finding the cheapist
            che=book
    # finally displaying these books
    print(f"The most expensive book is '{exp['Title']}' with price: {'%.2f'%float(exp['Price'])} QR\n")
    print(f"The least expensive book is '{che['Title']}' with price: {'%.2f'%float(che['Price'])} QR\n")

def getstockvalue(lstofbooks):
    """Calculates the stock value by summing price*copies for each book."""
    stockvalue=0
    for book in lstofbooks:
        stockvalue+=float(book['Price'])*int(book['Copies'])
    # returnint the stock value as a text in Qatari Rial
    return '%.2f'%stockvalue+" Qatari Rials"

def oldandlate(lstofbooks):
    """Aims to find the some of the oldest and newest books in the stock."""
    years=[]
    for book in lstofbooks:
        years.append(book['Year']) # gathering books' publishing year
    years.sort() # sorting those years

    old,new=[],[]
    for book in lstofbooks:
        if book['Year']==years[0]:# if a book is old enough
            if len(old)<3:# and if the list of old books is not full
                old.append(book)
        if book['Year']==years[-1]: # if a book is new
            if len(new)<3:# and if the list of new books is not full
                new.append(book)
        if len(new)==3 and len(old)==3: # break the loop if the two lists are full
            break
    # displaying the top threes in a nice tabular form
    print('Three of the oldest stocked books: ')
    print('',*books2lines(old,True,False))
    print('-'*50)
    print('Three of the latest stocked books: ')
    print('',*books2lines(new,True,False))

def leaststocked(lstofbooks):
    """Finds the least stocked books based on the least number of copies available."""
    #This may change in the future to limit the number of copies to be taken into concern
    copies=[]
    # finding the least number of copies
    for book in lstofbooks:
        copies.append(int(book['Copies']))
    copies.sort()
    
    least=[]
    # gathering the books that have the least number of copies
    for book in lstofbooks:
        if int(book['Copies']) == copies[0]:
            least.append(book)

    # Listing the least stocked book(s)
    print(f'The least stocked book(s) with number of copies: {copies[0]}\n','^'*50)
    for b in least:
        print(f"{b['ISBN']} | {b['Title']}")
    print('-'*50)


def showstatistics(stock):
    """Shows the stock statistics with the help of other functions."""
    print(f'The current value of the stock is: {getstockvalue(stock)}\n')
    print(f'The average book price is: {calcAvg(stock)} QR\n')
    expandche(stock) # the most and least expensive books
    leaststocked(stock) # the least stocked books
    oldandlate(stock) # some of the oldest/newest books

