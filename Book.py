class Book:
    def __init__(self, title: str, author: str, cost: int):
        """
        Create a book object with the given title, author, and cost
        """
        self.__title = title
        self.__author = author
        self.__cost = cost
        self.__section = None
    def getTitle(self):
        """
        Returns the title of the book
        """
        return self.__title
    def getAuthor(self):
        """
        Returns the name of the author of the book
        """
        return self.__author
    def getCost(self):
        """
        Returns the cost of the book
        """
        return self.__cost
    def getSection(self):
        """
        Returns the section of the book
        """
        return self.__section
    def setSection(self, section):
        """
        Sets the section of the book
        """
        self.__section = section