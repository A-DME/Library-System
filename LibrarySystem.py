from StockMethods import *

def main():
    """The main program."""
    programTitle='Bookstore Information System'
    MenuItems=['Add book details','Update a book','Delete a book','List stocked books','Find a book by ISBN',
                'Find books by a given publisher','Find books by a given author','Books above the average price',
                'Stock statistics','Exit']
    choices=['0','1','2','3','4','5','6','7','8','9']
    while True:
        inventory=getstock()
        print(f'\t{programTitle}')
        for i in range(len(MenuItems)):
            print(f'\t\t[{i+1}] {MenuItems[i]}') if i !=9 else print(f'\n\t\t[{0}] {MenuItems[i]}')
        choice=input('\tEnter your choice: ')
        if choice.strip() not in choices:
            print('Invalid choice. Try again!\n\n')
            continue
        if choice.strip() == choices[0]:
            break
        choiceMessage= programTitle +' - '+ MenuItems[int(choice)-1] + ':'
        print(choiceMessage)
        print('='*len(choiceMessage))
        if choice.strip() == choices[1]: add_book(inventory)
        elif choice.strip() == choices[2]: update_book(inventory)
        elif choice.strip() == choices[3]: delete_book(inventory)
        elif choice.strip() == choices[4]: print('',*books2lines(inventory,True,True))
        elif choice.strip() == choices[5]: findByCode(inventory)
        elif choice.strip() == choices[6]: booksByPublisher(inventory)
        elif choice.strip() == choices[7]: booksByAuthor(inventory)
        elif choice.strip() == choices[8]: listAboveAvg(inventory)
        elif choice.strip() == choices[9]: showstatistics(inventory)
        print('\n\n')
        

main()
