"""
Database operations for the Library Management System.
"""

import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    def __init__(self):
        """Initialize database connection."""
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establish database connection."""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
            print("Successfully connected to the database.")
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            raise

    def disconnect(self):
        """Close database connection."""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """Execute a SQL query with optional parameters."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return False

    def fetch_all(self, query, params=None):
        """Fetch all results from a query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def fetch_one(self, query, params=None):
        """Fetch a single result from a query."""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def create_tables(self):
        """Create all necessary database tables."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS categories (
                category_id INT PRIMARY KEY AUTO_INCREMENT,
                category_name VARCHAR(100) NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS books (
                book_id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(200) NOT NULL,
                isbn BIGINT UNIQUE NOT NULL,
                publish_year YEAR,
                category_id INT,
                author VARCHAR(100),
                FOREIGN KEY (category_id) REFERENCES categories(category_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS book_copies (
                copy_id INT PRIMARY KEY AUTO_INCREMENT,
                book_id INT NOT NULL,
                available CHAR(3) DEFAULT 'yes',
                condition_description VARCHAR(255),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS membership (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone CHAR(10),
                address VARCHAR(255),
                join_date DATE,
                expire_date DATE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS librarians (
                librarian_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                hire_date DATE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                copy_id INT NOT NULL,
                librarian_id INT NOT NULL,
                borrow_date DATE NOT NULL,
                return_date DATE DEFAULT NULL,
                due_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES membership(user_id),
                FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id),
                FOREIGN KEY (librarian_id) REFERENCES librarians(librarian_id)
            );
            """
        ]

        for query in queries:
            self.execute_query(query) 