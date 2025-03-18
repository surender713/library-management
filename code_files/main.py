"""
Main entry point for the Library Management System.
"""

from database import Database
from services import LibraryService
from config import APP_NAME, VERSION

def display_menu():
    """Display the main menu options."""
    print(f"\n{APP_NAME} v{VERSION}")
    print("=" * 50)
    print("1. Book Management")
    print("2. Member Management")
    print("3. Transaction Management")
    print("4. Reports")
    print("5. Exit")
    print("=" * 50)

def display_book_menu():
    """Display book management menu options."""
    print("\nBook Management")
    print("=" * 30)
    print("1. Add New Book")
    print("2. Add Book Copy")
    print("3. View All Books")
    print("4. Search Books")
    print("5. Back to Main Menu")
    print("=" * 30)

def display_member_menu():
    """Display member management menu options."""
    print("\nMember Management")
    print("=" * 30)
    print("1. Register New Member")
    print("2. View All Members")
    print("3. Search Members")
    print("4. Back to Main Menu")
    print("=" * 30)

def display_transaction_menu():
    """Display transaction management menu options."""
    print("\nTransaction Management")
    print("=" * 30)
    print("1. Borrow Book")
    print("2. Return Book")
    print("3. View Active Transactions")
    print("4. View Transaction History")
    print("5. Back to Main Menu")
    print("=" * 30)

def display_report_menu():
    """Display report menu options."""
    print("\nReports")
    print("=" * 30)
    print("1. Overdue Books")
    print("2. Popular Books")
    print("3. Member Activity")
    print("4. Back to Main Menu")
    print("=" * 30)

def main():
    """Main entry point of the application."""
    try:
        # Initialize database and service
        db = Database()
        db.create_tables()
        library_service = LibraryService()

        while True:
            display_menu()
            choice = input("\nEnter your choice (1-5): ")

            if choice == '1':
                while True:
                    display_book_menu()
                    book_choice = input("\nEnter your choice (1-5): ")
                    
                    if book_choice == '1':
                        # Add new book
                        title = input("Enter book title: ")
                        isbn = input("Enter ISBN: ")
                        publish_year = int(input("Enter publish year: "))
                        category_id = int(input("Enter category ID: "))
                        author = input("Enter author name: ")
                        library_service.add_book(title, isbn, publish_year, category_id, author)
                    
                    elif book_choice == '2':
                        # Add book copy
                        book_id = int(input("Enter book ID: "))
                        condition = input("Enter book condition: ")
                        library_service.add_book_copy(book_id, condition)
                    
                    elif book_choice == '3':
                        # View all books
                        library_service.display_books()
                    
                    elif book_choice == '4':
                        # Search books (to be implemented)
                        print("Search functionality coming soon...")
                    
                    elif book_choice == '5':
                        break

            elif choice == '2':
                while True:
                    display_member_menu()
                    member_choice = input("\nEnter your choice (1-4): ")
                    
                    if member_choice == '1':
                        # Register new member
                        name = input("Enter member name: ")
                        email = input("Enter email: ")
                        phone = input("Enter phone number: ")
                        address = input("Enter address: ")
                        library_service.register_member(name, email, phone, address)
                    
                    elif member_choice == '2':
                        # View all members (to be implemented)
                        print("View members functionality coming soon...")
                    
                    elif member_choice == '3':
                        # Search members (to be implemented)
                        print("Search functionality coming soon...")
                    
                    elif member_choice == '4':
                        break

            elif choice == '3':
                while True:
                    display_transaction_menu()
                    trans_choice = input("\nEnter your choice (1-5): ")
                    
                    if trans_choice == '1':
                        # Borrow book
                        user_id = int(input("Enter user ID: "))
                        copy_id = int(input("Enter book copy ID: "))
                        librarian_id = int(input("Enter librarian ID: "))
                        library_service.borrow_book(user_id, copy_id, librarian_id)
                    
                    elif trans_choice == '2':
                        # Return book
                        transaction_id = int(input("Enter transaction ID: "))
                        librarian_id = int(input("Enter librarian ID: "))
                        library_service.return_book(transaction_id, librarian_id)
                    
                    elif trans_choice == '3':
                        # View active transactions (to be implemented)
                        print("Active transactions view coming soon...")
                    
                    elif trans_choice == '4':
                        # View transaction history (to be implemented)
                        print("Transaction history view coming soon...")
                    
                    elif trans_choice == '5':
                        break

            elif choice == '4':
                while True:
                    display_report_menu()
                    report_choice = input("\nEnter your choice (1-4): ")
                    
                    if report_choice == '1':
                        # View overdue books
                        library_service.display_overdue_books()
                    
                    elif report_choice == '2':
                        # Popular books report (to be implemented)
                        print("Popular books report coming soon...")
                    
                    elif report_choice == '3':
                        # Member activity report (to be implemented)
                        print("Member activity report coming soon...")
                    
                    elif report_choice == '4':
                        break

            elif choice == '5':
                print("\nThank you for using the Library Management System!")
                break

            else:
                print("\nInvalid choice. Please try again.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()

