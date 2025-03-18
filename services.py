"""
Business logic and operations for the Library Management System.
"""

from datetime import datetime, timedelta
from prettytable import PrettyTable
from database import Database
from models import Book, Member, Transaction, Librarian, ValidationError

class LibraryService:
    def __init__(self):
        """Initialize library service with database connection."""
        self.db = Database()

    def add_book(self, title, isbn, publish_year, category_id, author):
        """Add a new book to the library."""
        try:
            # Validate book data
            title = Book.validate_title(title)
            isbn = Book.validate_isbn(isbn)
            publish_year = Book.validate_publish_year(publish_year)

            # Insert book
            query = """
                INSERT INTO books (title, isbn, publish_year, category_id, author)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (title, isbn, publish_year, category_id, author)
            
            if self.db.execute_query(query, params):
                print("Book added successfully.")
                return True
            return False
        except ValidationError as e:
            print(f"Validation error: {e}")
            return False
        except Exception as e:
            print(f"Error adding book: {e}")
            return False

    def add_book_copy(self, book_id, condition_description):
        """Add a new copy of an existing book."""
        try:
            query = """
                INSERT INTO book_copies (book_id, condition_description)
                VALUES (%s, %s)
            """
            params = (book_id, condition_description)
            
            if self.db.execute_query(query, params):
                print("Book copy added successfully.")
                return True
            return False
        except Exception as e:
            print(f"Error adding book copy: {e}")
            return False

    def register_member(self, name, email, phone, address):
        """Register a new library member."""
        try:
            # Validate member data
            name = Member.validate_name(name)
            email = Member.validate_email(email)
            phone = Member.validate_phone(phone)
            address = Member.validate_address(address)

            # Set membership dates
            join_date = datetime.now()
            expire_date = join_date + timedelta(days=365)

            query = """
                INSERT INTO membership (name, email, phone, address, join_date, expire_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (name, email, phone, address, join_date, expire_date)
            
            if self.db.execute_query(query, params):
                print("Member registered successfully.")
                return True
            return False
        except ValidationError as e:
            print(f"Validation error: {e}")
            return False
        except Exception as e:
            print(f"Error registering member: {e}")
            return False

    def borrow_book(self, user_id, copy_id, librarian_id):
        """Process a book borrowing transaction."""
        try:
            # Check if book is available
            if not self.is_book_available(copy_id):
                print("Book is not available for borrowing.")
                return False

            # Check if user has reached maximum books limit
            if not self.can_user_borrow(user_id):
                print("User has reached maximum books limit.")
                return False

            # Set transaction dates
            borrow_date = datetime.now()
            due_date = Transaction.calculate_due_date()

            query = """
                INSERT INTO transactions (user_id, copy_id, librarian_id, borrow_date, due_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (user_id, copy_id, librarian_id, borrow_date, due_date)
            
            if self.db.execute_query(query, params):
                # Update book availability
                self.update_book_availability(copy_id, 'no')
                print("Book borrowed successfully.")
                return True
            return False
        except Exception as e:
            print(f"Error borrowing book: {e}")
            return False

    def return_book(self, transaction_id, librarian_id):
        """Process a book return transaction."""
        try:
            # Get transaction details
            query = "SELECT copy_id FROM transactions WHERE transaction_id = %s"
            result = self.db.fetch_one(query, (transaction_id,))
            if not result:
                print("Transaction not found.")
                return False

            copy_id = result[0]
            return_date = datetime.now()

            # Update transaction
            query = """
                UPDATE transactions 
                SET return_date = %s, librarian_id = %s
                WHERE transaction_id = %s
            """
            params = (return_date, librarian_id, transaction_id)
            
            if self.db.execute_query(query, params):
                # Update book availability
                self.update_book_availability(copy_id, 'yes')
                print("Book returned successfully.")
                return True
            return False
        except Exception as e:
            print(f"Error returning book: {e}")
            return False

    def is_book_available(self, copy_id):
        """Check if a book copy is available."""
        query = "SELECT available FROM book_copies WHERE copy_id = %s"
        result = self.db.fetch_one(query, (copy_id,))
        return result and result[0] == 'yes'

    def can_user_borrow(self, user_id):
        """Check if a user can borrow more books."""
        query = """
            SELECT COUNT(*) FROM transactions 
            WHERE user_id = %s AND return_date IS NULL
        """
        result = self.db.fetch_one(query, (user_id,))
        return result and result[0] < 3  # Maximum 3 books per user

    def update_book_availability(self, copy_id, status):
        """Update book copy availability status."""
        query = "UPDATE book_copies SET available = %s WHERE copy_id = %s"
        return self.db.execute_query(query, (status, copy_id))

    def display_books(self):
        """Display all books in a formatted table."""
        query = """
            SELECT b.book_id, b.title, b.isbn, b.publish_year, c.category_name, b.author,
                   COUNT(bc.copy_id) as total_copies,
                   SUM(CASE WHEN bc.available = 'yes' THEN 1 ELSE 0 END) as available_copies
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.category_id
            LEFT JOIN book_copies bc ON b.book_id = bc.book_id
            GROUP BY b.book_id
        """
        results = self.db.fetch_all(query)
        
        table = PrettyTable()
        table.field_names = ["ID", "Title", "ISBN", "Year", "Category", "Author", "Total", "Available"]
        table.add_rows(results)
        print(table)

    def display_overdue_books(self):
        """Display all overdue books in a formatted table."""
        query = """
            SELECT t.transaction_id, b.title, m.name as member_name, t.borrow_date, t.due_date
            FROM transactions t
            JOIN book_copies bc ON t.copy_id = bc.copy_id
            JOIN books b ON bc.book_id = b.book_id
            JOIN membership m ON t.user_id = m.user_id
            WHERE t.return_date IS NULL AND t.due_date < CURDATE()
        """
        results = self.db.fetch_all(query)
        
        table = PrettyTable()
        table.field_names = ["Transaction ID", "Book", "Member", "Borrow Date", "Due Date"]
        table.add_rows(results)
        print(table) 