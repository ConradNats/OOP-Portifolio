# library/books.py

books = []


def add_book(title):
    books.append(title)
    return f"'{title}' added successfully."


def search_book(title):
    if title in books:
        return f"'{title}' is available."
    return f"'{title}' was not found."


def check_availability(title):
    return title in books

add_book("Titans")