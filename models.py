from typing import List, Optional, Dict
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']
books_collection = db['books']

class Book:
    def __init__(self, title: str, category: str, author: str, cover: str, price: float, poster: str, year: int, count: int, _id: Optional[ObjectId] = None):
        """
        Инициализирует объект книги.

        Args:
            title (str): Название книги.
            category (str): Категория книги.
            author (str): Автор книги.
            cover (str): URL обложки книги.
            price (float): Цена книги.
            poster (str): URL постера книги.
            year (int): Год издания книги.
            count (int): Количество книг в наличии.
            _id (Optional[ObjectId]): Идентификатор книги. Если не указан, генерируется новый ObjectId.
        """
        self._id = _id or ObjectId()
        self.title = title
        self.category = category
        self.author = author
        self.cover = cover
        self.price = price
        self.poster = poster
        self.year = year
        self.count = count

    def save(self) -> None:
        """
        Сохраняет книгу в базу данных.
        """
        books_collection.insert_one(self.__dict__)

    @staticmethod
    def get_all() -> List[Dict]:
        """
        Получает список всех книг из базы данных.

        Returns:
            List[Dict]: Список книг в виде словарей.
        """
        return list(books_collection.find())

    @staticmethod
    def get_by_id(book_id: str) -> Optional[Dict]:
        """
        Получает книгу по её идентификатору.

        Args:
            book_id (str): Идентификатор книги.

        Returns:
            Optional[Dict]: Словарь с данными книги, если она найдена, иначе None.
        """
        return books_collection.find_one({"_id": ObjectId(book_id)})

    @staticmethod
    def update(book_id: str, update_data: Dict) -> None:
        """
        Обновляет данные книги в базе данных.

        Args:
            book_id (str): Идентификатор книги.
            update_data (Dict): Словарь с обновленными данными книги.
        """
        books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": update_data})

    @staticmethod
    def delete(book_id: str) -> None:
        """
        Удаляет книгу из базы данных.

        Args:
            book_id (str): Идентификатор книги.
        """
        books_collection.delete_one({"_id": ObjectId(book_id)})

    @staticmethod
    def delete_all() -> None:
        """
        Удаляет все книги из базы данных.
        """
        books_collection.delete_many({})
