from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QLineEdit, QPushButton, QGridLayout, QTabWidget, QListWidget, QListWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
import sys
from Library import Library

LOAD_DATA_FROM_FIREBASE = False # Set this to False if you want to load data from local json file instead of firebase
                               # Setting this to false will result in the app not saving data to firebase

class CURTBookStoreApp(QDialog):
    def __init__(self):
        super(CURTBookStoreApp, self).__init__()

        # Load the ui file
        uic.loadUi("CURT.ui", self)
        # Load the library
        self.library = Library("CURT - Bookstore", load_from_firebase=LOAD_DATA_FROM_FIREBASE)
        if LOAD_DATA_FROM_FIREBASE:
            self.loadSoldBooks()
        # book holder
        self.__current_book = None
        self.__current_sold_book = None
        # Define Library Tab Widgets
            # Search text boxes
        self.bookTitleLineEdit = self.findChild(QLineEdit, "bookTitleLineEdit")
        self.authorLineEdit = self.findChild(QLineEdit, "authorLineEdit")
        self.bookTypeLineEdit = self.findChild(QLineEdit, "bookTypeLineEdit")
            # Available Books List
        self.avBooks_list = self.findChild(QListWidget, "avBooks_list")
            # Buy Button
        self.buyBook_pButton = self.findChild(QPushButton, "buyBook_pButton")
            # Book info labels
        self.inf_name_label = self.findChild(QLabel, "inf_name_label")
        self.inf_author_label = self.findChild(QLabel, "inf_author_label")
        self.inf_section_label = self.findChild(QLabel, "inf_section_label")
        self.inf_cost_label = self.findChild(QLabel, "inf_cost_label")
            # Error labels
        self.label_failed = self.findChild(QLabel, "label_failed")
        self.label_done = self.findChild(QLabel, "label_done")

        
        # Define Profit Tab Widgets
            # Sold Books List
        self.soldBooks_list = self.findChild(QListWidget, "soldBooks_list")
            # Total Books Sold and Profit Labels
        self.tBooks_sold_label = self.findChild(QLabel, "tBooks_sold_label")
        self.tProfit_label = self.findChild(QLabel, "tProfit_label")
            # Return Book Button
        self.returnBook_pButton = self.findChild(QPushButton, "returnBook_pButton")
            # Error labels
        self.label_failed_2 = self.findChild(QLabel, "label_failed_2")
        self.label_done_2 = self.findChild(QLabel, "label_done_2")

        # Load books from library
        self.loadBooks()
        # Functionalities & events
            # Library Tab
        self.buyBook_pButton.clicked.connect(self.buyBook)
        self.avBooks_list.itemClicked.connect(self.showBookInfo)
        for ledit in [self.bookTitleLineEdit, self.authorLineEdit, self.bookTypeLineEdit]:
            ledit.textChanged.connect(self.searchBooks)
            # Profit Tab
        self.soldBooks_list.itemClicked.connect(self.selectSoldBook)
        self.returnBook_pButton.clicked.connect(self.returnBook)

        # Show The App
        self.show()

    
    def searchBooks(self):
        """
        Search books from library
        """
        self.avBooks_list.clear()
        sections = self.library.getSections()
        last_row = 0
        for section in sections:
            books = section.showBooks()
            section_item = QListWidgetItem()
            section_item.setText(f" - {section.getTitle()}")
            # change item text color from color hash code
            brush = QBrush(QColor(74, 74, 74))
            section_item.setForeground(brush)
            section_item.setFlags(Qt.NoItemFlags) # Make sections unselectable & with different color
            self.avBooks_list.addItem(section_item)
            last_row += 1
            books_found = 0
            for book in books:
                if self.bookTitleLineEdit.text().lower().replace(' ', '') in book.getTitle().lower().replace(' ', '') and self.authorLineEdit.text().lower().replace(' ', '') in book.getAuthor().lower().replace(' ', '') and self.bookTypeLineEdit.text().lower().replace(' ', '') in book.getSection().getTitle().lower().replace(' ', ''):
                    self.avBooks_list.addItem(book.getTitle()+" - By "+book.getAuthor())
                    books_found += 1
                    last_row += 1
            if books_found == 0:
                self.avBooks_list.takeItem(last_row-1)
                last_row -= 1


    def loadBooks(self):
        """
        Load books from library
        """
        # instead of implemeting a different method to load books from
        # instead, we load books from library by searching with empty text boxes
        return self.searchBooks()

    def showBookInfo(self):
        """
        Show book info on book selection
        """
        selected_item = self.avBooks_list.currentItem()
        book = self.library.searchBookByTitle(selected_item.text().split(" - By")[0])[0] if selected_item else None
        self.inf_name_label.setText(book.getTitle() if book else 'N/a')
        self.inf_author_label.setText(book.getAuthor() if book else 'N/a')
        self.inf_section_label.setText(book.getSection().getTitle() if book else 'N/a')
        self.inf_cost_label.setText(str(book.getCost())+"$" if book else '0$')
        if book:
            self.__current_book = book

    def buyBook(self):
        """
        Buy book from library
        """
        if self.__current_book:
            if self.library.sellaBook(self.__current_book.getTitle()):
                self.label_done.setText(f"You have successfully bought the book for {self.__current_book.getCost()}$")
                self.label_failed.setText("")
                self.tBooks_sold_label.setText(str(len(self.library.getSoldBooks())))
                self.tProfit_label.setText(str(self.library.getTotalProfit())+"$")
                sbook_item = QListWidgetItem()
                sbook_item.setText(f"{self.__current_book.getTitle()} ({self.__current_book.getCost()}$)")
                self.soldBooks_list.addItem(sbook_item)
                self.searchBooks() # refresh the list
                self.showBookInfo() # reset info labels
                self.__current_book = None

                if LOAD_DATA_FROM_FIREBASE:
                    self.library.getFirebaseLoader().saveAllData(self.library) # save data to firebase

            else:
                self.label_failed.setText("Please select a book from the list!")
                self.label_done.setText("")
        else:
            self.label_failed.setText("Please select a book from the list!")
            self.label_done.setText("")

    def selectSoldBook(self):
        """
        Select sold book from library
        """
        selected_item = self.soldBooks_list.currentItem()
        book = self.library.searchSoldBookByTitle(selected_item.text()) if selected_item else None
        self.__current_sold_book = book
    def returnBook(self):
        """
        Return a book
        """
        if self.__current_sold_book:
            print(self.__current_sold_book)
            self.library.returnaBook(self.__current_sold_book)
            self.loadSoldBooks() # refresh the list
            self.searchBooks() # refresh the list
            self.label_done_2.setText(f"You have successfully returned the book ({self.__current_sold_book.getCost()}$)")
            self.label_failed_2.setText("")
            self.__current_sold_book = None

            if LOAD_DATA_FROM_FIREBASE:
                    self.library.getFirebaseLoader().saveAllData(self.library) # save data to firebase
        else:
            self.label_failed_2.setText("Please select a book from the list!")
            self.label_done_2.setText("")
    def loadSoldBooks(self):
        """
        Load sold books from library
        """
        self.soldBooks_list.clear()
        sold_books = self.library.getSoldBooks()
        total_cost = 0
        for book in sold_books:
            sbook_item = QListWidgetItem()
            sbook_item.setText(f"{book.getTitle()} ({book.getCost()}$)")
            self.soldBooks_list.addItem(sbook_item)
            total_cost += book.getCost()
        
        self.tBooks_sold_label.setText(str(len(sold_books)))
        self.tProfit_label.setText(str(total_cost)+"$")

# Initialize The App
app = QApplication(sys.argv)
AppWindow = CURTBookStoreApp()
app.exec_()