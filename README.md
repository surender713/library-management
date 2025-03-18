# Library Management System

A comprehensive CLI-based application for managing library operations, including books, members, librarians, and transactions.

## Features

### Book Management
- Add, update, delete, and retrieve books
- Categorize books by genre
- Track book copies and their availability
- Manage book condition information

### Member Management
- Register new members with contact information
- Track membership validity (join date and expiry date)
- Manage member details (name, email, phone, address)

### Librarian Management
- Add and manage librarian information
- Track librarian hiring dates
- Associate librarians with transactions

### Transaction System
- Record book borrowing and returns
- Track due dates and return status
- Generate reports on overdue books
- Complete transaction history

## Tech Stack
- **Python**: Core programming language
- **MySQL**: Database system for data storage
- **mysql-connector-python**: Python library for MySQL connection
- **PrettyTable**: For formatted display of data in console

## Prerequisites
- Python 3.6 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your MySQL database:
   - Ensure MySQL server is running
   - Update the database connection parameters in `main.py`:
     ```python
     connection = mysql.connector.connect(
         host='localhost',
         user='your_username',
         password='your_password',
     )
     ```

4. Run the application:
```bash
python main.py
```

## Usage

The application provides a console-based menu with the following options:

1. **Add New Record**
   - Add Book Copy
   - Add Book
   - Add Category
   - Add Librarian
   - Add Transaction
   - Add Membership

2. **Retrieve Data**
   - View Books
   - View Members
   - View Transactions
   - View Available Books
   - View Overdue Books

3. **Update Record**
   - Update Book Information
   - Update Member Details
   - Update Transaction Status
   - Mark Book as Returned

4. **Delete Record**
   - Remove Book Records
   - Delete Member Information
   - Remove Transaction Records

## Database Schema

The database consists of the following tables:

- **categories**: Stores book categories/genres
- **books**: Contains book information with category reference
- **book_copies**: Manages individual copies of books and their status
- **membership**: Stores library member information
- **librarians**: Contains librarian details
- **transactions**: Records all borrowing and returning transactions

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Run tests
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- MySQL Documentation
- Python MySQL Connector Documentation
- PrettyTable Documentation 