import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), nullable=False)

    books = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'Publisher {self.id}: {self.name}'


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), nullable=False)

    books = relationship('Stock', backref='shop')

    def __str__(self):
        return f'Shop {self.id}: {self.name}'


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship('Publisher', back_populates='books')
    shops = relationship('Stock', backref='book')

    def __str__(self):
        return f'Book {self.id}: {self.title}, id издателя - {self.id_publisher}'


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    sales = relationship('Sale', back_populates='stock')

    def __str__(self):
        return f'Stock {self.id}: id книги - {self.id_book}, id магазина - {self.id_shop}, количество - {self.count}'


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DATE, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship('Stock', back_populates='sales')

    def __str__(self):
        return f'Sale {self.id}: цена - {self.price}, дата - {self.date_sale}, id покупки - {self.id_stock}, \
        количество - {self.count}'


def create_table(engine):
    """Функция создает таблицу в базе данных"""
    Base.metadata.create_all(engine)
    print('Таблицы созданы')


def drop_table(engine):
    """Функция удаляет все таблицы из базы данных"""
    Base.metadata.drop_all(engine)
    print('Таблицы удалены')
