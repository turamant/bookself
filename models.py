from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']
books_collection = db['books']

class Book:
    def __init__(self, title, category, author, cover, price, poster, year, count, _id=None):
        self._id = _id or ObjectId()  # Generate a new ObjectId if not provided
        self.title = title
        self.category = category
        self.author = author
        self.cover = cover
        self.price = price
        self.poster = poster
        self.year = year
        self.count = count

    def save(self):
        books_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all():
        return list(books_collection.find())

    @staticmethod
    def get_by_id(book_id):
        return books_collection.find_one({"_id": ObjectId(book_id)})
    

    @staticmethod
    def update(book_id, update_data):
        books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})
    
    @staticmethod
    def delete(book_id):
        books_collection.delete_one({"_id": ObjectId(book_id)})
