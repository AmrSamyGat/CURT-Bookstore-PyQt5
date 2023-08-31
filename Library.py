from Section import Section
from Book import Book
from json import load
from FireBaseLoader import FireBaseLoader

class Library:
    def __init__(self, title: str, load_from_firebase: bool = False):
        """
        Initiate a library object with the given name
        """
        self.__title = title
        self.__sections = []
        self.__sold_books = []
        self.__profit = 0
        self.__firebase_loader = FireBaseLoader()
        
        if load_from_firebase and self.__firebase_loader.isDataAvailable():
            self.__firebase_loader.loadDataIntoLibrary(self)
            print("Loaded data from firebase")
        else:
            with open('books.json', 'r') as lf:
                __library_data = load(lf)
                __loaded_books = 0
                for book_name, book_data in __library_data.items():
                    b_section = self.getSectionByName(book_data['section'])
                    if b_section == None:
                        b_section = Section(book_data['section'])
                        self.addSection(b_section)
                    b_section.addBook(Book(book_name, book_data['author'], book_data['cost']))
                    __loaded_books += 1
                print(f'Loaded {len(self.__sections)} and {__loaded_books} books in Library {self.__title}')
    def addSection(self, section: Section):
        """
        Adds the given section to the library
        """
        self.__sections.append(section)
    def searchBookByTitle(self, title: str):
        """
        Searches for a book with the given title in all sections
        """
        results = []
        for section in self.__sections:
            results += section.searchBookByTitle(title)
        return results
    def searchBookByAuthor(self, author: str):
        """
        Searches for a book with the given author name in all sections
        """
        results = []
        for section in self.__sections:
            results += section.searchBookByAuthor(author)
        return results
    def sellaBook(self, title: str):
        """
        Sells the book with the given title from the library
        """
        book_to_sell = self.searchBookByTitle(title)
        if len(book_to_sell) == 0:
            print('Book not found')
            return None
        else:
            self.__profit += book_to_sell[0].getCost()
            self.__sold_books.append(book_to_sell[0])
            for section in self.__sections:
                section.deleteBook(book_to_sell[0].getTitle())
            return True
    def returnaBook(self, book):
        """
        Returns the given book to the library
        """
        for section in self.__sections:
            if section.getTitle() == book.getSection().getTitle():
                section.addBook(book)
        self.__sold_books.remove(book)
        self.__profit -= book.getCost()
    def addBookToSold(self, book: Book):
        """
        Adds the given book to the sold books
        """
        self.__sold_books.append(book)
        self.__profit += book.getCost()
    def getTotalProfit(self):
        """
        Returns the total profit of the library
        """
        return self.__profit
    def getBooks(self):
        """
        Shows all the books in the library
        """
        results = []
        for section in self.__sections:
            results += section.showBooks()
        return results
    def getSoldBooks(self):
        """
        Returns a list of the sold books
        """
        return self.__sold_books
    def getSectionByName(self, name: str):
        """
        Returns the section with the given name
        """
        for section in self.__sections:
            if section.getTitle() == name:
                return section
        return None
    def getSections(self):
        """
        Returns all the sections in the library
        """
        return self.__sections

    def searchSoldBookByTitle(self, title: str):
        """
        Returns the sold book with the given title
        """
        for book in self.__sold_books:
            if book.getTitle().lower().replace(' ', '') in title.lower().replace(' ', ''):
                return book
        return None

    def getFirebaseLoader(self):
        """
        Returns the firebase loader
        """
        return self.__firebase_loader