"""
Data models and validation for the Library Management System.
"""

import re
from datetime import datetime, timedelta
from config import MAX_BOOKS_PER_USER, DEFAULT_BORROW_DURATION_DAYS

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class Book:
    """Book model with validation."""
    
    @staticmethod
    def validate_title(title):
        """Validate book title."""
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty")
        return title.strip()

    @staticmethod
    def validate_isbn(isbn):
        """Validate ISBN number."""
        if not str(isbn).isdigit() or len(str(isbn)) < 10:
            raise ValidationError("Invalid ISBN format")
        return isbn

    @staticmethod
    def validate_publish_year(year):
        """Validate publish year."""
        current_year = datetime.now().year
        if not isinstance(year, int) or year < 1800 or year > current_year:
            raise ValidationError(f"Invalid publish year. Must be between 1800 and {current_year}")
        return year

class Member:
    """Member model with validation."""
    
    @staticmethod
    def validate_name(name):
        """Validate member name."""
        if not name or not name.strip():
            raise ValidationError("Name cannot be empty")
        if not name.replace(" ", "").isalpha():
            raise ValidationError("Name should contain only letters and spaces")
        return name.strip()

    @staticmethod
    def validate_email(email):
        """Validate email address."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        return email.lower()

    @staticmethod
    def validate_phone(phone):
        """Validate phone number."""
        if not phone or not phone.strip():
            raise ValidationError("Phone number cannot be empty")
        if not phone.isdigit() or len(phone) != 10:
            raise ValidationError("Phone number must be 10 digits")
        if not phone[0] in '6789':
            raise ValidationError("Phone number must start with 6, 7, 8, or 9")
        return phone

    @staticmethod
    def validate_address(address):
        """Validate address."""
        if not address or not address.strip():
            raise ValidationError("Address cannot be empty")
        return address.strip()

class Transaction:
    """Transaction model with validation."""
    
    @staticmethod
    def calculate_due_date():
        """Calculate due date based on default duration."""
        return datetime.now() + timedelta(days=DEFAULT_BORROW_DURATION_DAYS)

    @staticmethod
    def validate_dates(borrow_date, due_date):
        """Validate transaction dates."""
        if not isinstance(borrow_date, datetime):
            borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d')
        if not isinstance(due_date, datetime):
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        
        if due_date <= borrow_date:
            raise ValidationError("Due date must be after borrow date")
        if due_date > borrow_date + timedelta(days=30):
            raise ValidationError("Maximum borrow duration is 30 days")
        return borrow_date, due_date

class Librarian:
    """Librarian model with validation."""
    
    @staticmethod
    def validate_name(name):
        """Validate librarian name."""
        return Member.validate_name(name)

    @staticmethod
    def validate_email(email):
        """Validate librarian email."""
        return Member.validate_email(email)

    @staticmethod
    def validate_hire_date(hire_date):
        """Validate hire date."""
        if not isinstance(hire_date, datetime):
            hire_date = datetime.strptime(hire_date, '%Y-%m-%d')
        if hire_date > datetime.now():
            raise ValidationError("Hire date cannot be in the future")
        return hire_date 