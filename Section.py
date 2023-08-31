from Book import Book

class Section:
    def __init__(self, title: str):
        """
        Create a section object with the given title
        """
        self.__title = title
        self.__books = []
    def getTitle(self):
        """
        Returns the title of the section
        """
        return self.__title
    def addBook(self, book: Book):
        """
        Adds the given book to the section
        """
        book.setSection(self)
        self.__books.append(book)
    def searchBookByTitle(self, title: str):
        """
        Searches for a book with the given title
        """
        results = []
        for book in self.__books:
            if title.lower().replace(' ', '') in book.getTitle().lower().replace(' ', ''):
                results.append(book)
        return results
    def searchBookByAuthor(self, author: str):
        """
        Searches for a book with the given author name
        """
        results = []
        for book in self.__books:
            if author.lower().replace(' ', '') in book.getAuthor().lower().replace(' ', ''):
                results.append(book)
        return results
    def deleteBook(self, title: str):
        """
        Deletes the book with the given title from the section
        """
        for book in self.__books:
            if book.getTitle().lower().replace(' ', '') == title.lower().replace(' ', ''):
                self.__books.remove(book)
    def showBooks(self):
        """
        Shows all the books in the section
        """
        for book in self.__books:
            print(book.getTitle(), book.getAuthor(), book.getCost())

        return self.__books