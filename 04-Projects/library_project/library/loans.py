# library/loans.py

def borrow_book(member, book):
    return f"{member} borrowed '{book}'."


def return_book(member, book):
    return f"{member} returned '{book}'."


def calculate_fine(days_late, rate=1000):
    return days_late * rate

