import pyrebase
from json import load
from Section import Section
from Book import Book

class FireBaseLoader:
    def __init__(self):
        """
        Initiate and connect to firebase and interact with it
        """
        with open('firebase_config.json', 'r') as f:
            self.__config = load(f)
        self.__firebase = pyrebase.initialize_app(self.__config)
        self.__db = self.__firebase.database()
    
    def getBooks(self):
        """
        Returns the books json from firebase
        """
        return self.__db.child('books').get().val()
    def getSoldBooks(self):
        """
        Returns the sold books json from firebase
        """
        return self.__db.child('sold_books').get().val()
    def getProfit(self):
        """
        Returns the profit json from firebase
        """
        return self.__db.child('profit').get().val()
    def saveAllData(self, library):
        """
        Saves all the data to firebase
        """
        books = library.getBooks()
        sold_books = library.getSoldBooks()
        profit = library.getTotalProfit()
        books_jsonable = {}
        sold_books_jsonable = {}
        for book in books:
            books_jsonable[book.getTitle()] = {
                'author': book.getAuthor(),
                'cost': book.getCost(),
                'section': book.getSection().getTitle()
            }
        for book in sold_books:
            sold_books_jsonable[book.getTitle()] = {
                'author': book.getAuthor(),
                'cost': book.getCost(),
                'section': book.getSection().getTitle()
            }
        self.__db.child('books').set(books_jsonable)
        self.__db.child('sold_books').set(sold_books_jsonable)
        self.__db.child('profit').set(profit)
        print('Data saved successfully')

    def loadDataIntoLibrary(self, library):
        """
        Loads all the data from firebase into the library
        """
        books = self.getBooks()
        sold_books = self.getSoldBooks()
        profit = self.getProfit()
        if books:
            for book_name, book_data in books.items():
                b_section = library.getSectionByName(book_data['section'])
                if b_section == None:
                    b_section = Section(book_data['section'])
                    library.addSection(b_section)
                b_section.addBook(Book(book_name, book_data['author'], book_data['cost']))
        
        if sold_books:
            for book_name, book_data in sold_books.items():
                b_section = library.getSectionByName(book_data['section'])
                if b_section == None:
                    b_section = Section(book_data['section'])
                    library.addSection(b_section)
                sbook = Book(book_name, book_data['author'], book_data['cost'])
                sbook.setSection(b_section)
                library.addBookToSold(sbook)
        
        print('Data loaded successfully')

    def isDataAvailable(self):
        """
        Returns True if data is available in firebase
        """
        return (self.getBooks() != None or self.getSoldBooks() != None) and self.getProfit() != None 