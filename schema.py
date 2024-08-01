import graphene
from models import Book as BookModel

class BookType(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    category = graphene.String()
    author = graphene.String()
    cover = graphene.String()
    price = graphene.Float()
    poster = graphene.String()
    year = graphene.Int()
    count = graphene.Int()

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)
    book = graphene.Field(BookType, book_id=graphene.String())

    def resolve_all_books(self, info):
        books = BookModel.get_all()
        return [BookType(
            id=str(book['_id']),
            title=book['title'],
            category=book['category'],
            author=book['author'],
            cover=book['cover'],
            price=book['price'],
            poster=book['poster'],
            year=book['year'],
            count=book['count']
        ) for book in books]
        
    def resolve_book(self, info, book_id):
        book = BookModel.get_by_id(book_id)
        if book:
            return BookType(
                id=str(book['_id']),
                title=book['title'],
                category=book['category'],
                author=book['author'],
                cover=book['cover'],
                price=book['price'],
                poster=book['poster'],
                year=book['year'],
                count=book['count']
            )
        else:
            return None

class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        category = graphene.String(required=True)
        author = graphene.String(required=True)
        cover = graphene.String(required=True)
        price = graphene.Float(required=True)
        poster = graphene.String(required=True)
        year = graphene.Int(required=True)
        count = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, category, author, cover, price, poster, year, count):
        # Create a new book instance
        book = BookModel(title, category, author, cover, price, poster, year, count)
        book.save()
        # Create a BookType instance with the correct fields
        return CreateBook(book=BookType(
            id=str(book._id),
            title=book.title,
            category=book.category,
            author=book.author,
            cover=book.cover,
            price=book.price,
            poster=book.poster,
            year=book.year,
            count=book.count
        ))
        
        
class UpdateBook(graphene.Mutation):
    class Arguments:
        book_id = graphene.String(required=True)
        title = graphene.String()
        category = graphene.String()
        author = graphene.String()
        cover = graphene.String()
        price = graphene.Float()
        poster = graphene.String()
        year = graphene.Int()
        count = graphene.Int()

    book = graphene.Field(BookType)

    def mutate(self, info, book_id, title=None, category=None, author=None, cover=None, price=None, poster=None, year=None, count=None):
        # Обновляем книгу в базе данных
        update_data = {
            "title": title,
            "category": category,
            "author": author,
            "cover": cover,
            "price": price,
            "poster": poster,
            "year": year,
            "count": count
        }
        BookModel.update(book_id, update_data)

        # Получаем обновленную книгу из базы данных
        book = BookModel.get_by_id(book_id)

        # Возвращаем обновленную книгу в виде BookType
        return UpdateBook(book=BookType(
            id=str(book['_id']),
            title=book['title'],
            category=book['category'],
            author=book['author'],
            cover=book['cover'],
            price=book['price'],
            poster=book['poster'],
            year=book['year'],
            count=book['count']
        ))

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
