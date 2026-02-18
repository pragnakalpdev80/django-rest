# # Basic function
# def greet(name):
#     return f"Hello, {name}!"

# # Function with multiple parameters
# def create_book(title, author, price):
#     book ={
#         "title": title,
#         "author": author,
#         "price": price}
#     return book

# # Function that processes data (like an API endpoint)
# def get_book_info(book_id):
#     # In a real API, this would fetch from database
#     if book_id == 1:
#         return {"id": 1, "title": "Python Guide", "author": "John"}
#     else:
#         return None

# # Using functions
# result = greet("Alice")
# book = create_book("Django Guide", "Jane", 39.99)
# info = get_book_info(1)

# print(result,book,info)

# # Define a class (like a blueprint)
# class Book:
#     def __init__(self, title, author, price):
#         # __init__ is called when creating an object
#         self.title = title
#         self.author = author
#         self.price = price
    
#     def get_info(self):
#         # Method (function inside a class)
#         return f"{self.title} by {self.author} - ${self.price}"

# # Create objects (instances) from the class
# book1 = Book("Python Guide", "John", 29.99)
# book2 = Book("Django Guide", "Jane", 39.99)

# # Use the objects
# print(book1.get_info())  # "Python Guide by John - $29.99"
# print(book2.title)       # "Django Guide"

# # Import entire module
# import json
# import datetime

# # Import specific functions/classes
# from datetime import date
# from json import loads, dumps

# # Import with alias
# import django.db.models as models

# # Using imports
# today = date.today()
# data = loads('{"key": "value"}')  # Parse JSON string

# def format_book(book):
#     return f"{book['title']} by {book['author']} - ${book['price']}"

# book1 = {"id": 1, "title": "Python Guide", "author": "John", "price": 29.99}
# book2 = {"id": 2, "title": "Django Guide", "author": "Jane", "price": 39.99}
# book3 = {"id": 3, "title": "DRF Guide", "author": "Bob", "price": 49.99}

# books = [book1, book2, book3]

# for book in books:
#     print(format_book(book))

import json

book ={
    "id": 1,
    "title": "Python Guide",
    "author": "John Doe",
    "price": 29.99,
    "published": True}

# Convert to JSON
json_string = json.dumps(book)
print("JSON:", json_string)

# Convert back to dict
book_dict = json.loads(json_string)
print("Dictionary:", book_dict)