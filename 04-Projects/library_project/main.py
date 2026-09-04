# main.py

from library.books import add_book, search_book
from library.members import register_member, search_member
from library.loans import borrow_book, return_book, calculate_fine


def main():

    print("===== LIBRARY MANAGEMENT SYSTEM =====")

    # Add books
    print(add_book("Python Basics"))
    print(add_book("Data Science"))
    print(add_book("Machine Learning"))
    print(add_book("Deep Learning"))

    # Register members
    print(register_member("Conrad"))
    print(register_member("Amina"))
    print(register_member("Jill"))

    # Search
    print(search_book("Python Basics"))
    print(search_book("Machine Learning"))
    print(search_member("Conrad"))

    # Borrow
    print(borrow_book("Conrad", "Python Basics"))

    # Return
    print(return_book("Conrad", "Python Basics"))

    # Fine
    fine = calculate_fine(3)
    print(f"Fine: UGX {fine}")
    
    print(search_book("Machine learning"))
    

if __name__ == "__main__":
    main()