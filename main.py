import sqlalchemy
import json
import os
from sqlalchemy.orm import sessionmaker
from models import Publisher, Shop, Book, Stock, Sale, create_table, drop_table


login = os.getenv('login')
password = os.getenv('password')
db_name = os.getenv('db_name')
DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def select_sale():
    """Функция выводит факты покупки книг издателя по его имени или идентификатору"""
    name = input('Введите имя издателя или его идентификатор: ')
    try:
        for c in session.query(
                Book.title, Shop.name, Sale.price, Sale.date_sale
        ).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.id == int(name)).all():
            print(' | '.join(str(i) for i in c))
    except ValueError:
        for c in session.query(
                Book.title, Shop.name, Sale.price, Sale.date_sale
        ).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name == name).all():
            print(' | '.join(str(i) for i in c))


if __name__ == '__main__':
    drop_table(engine)
    create_table(engine)

    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))

    pb = Publisher(id=5, name='Пушкин')
    sh = Shop(id=4, name='Буквоед')
    sh1 = Shop(id=5, name='Лабиринт')
    bk = Book(id=7, title='Капитанская дочка', id_publisher=5)
    bk1 = Book(id=8, title='Руслан и Людмила', id_publisher=5)
    bk2 = Book(id=9, title='Евгений Онегин', id_publisher=5)
    st = Stock(id=10, id_book=7, id_shop=4, count=10)
    st1 = Stock(id=11, id_book=7, id_shop=5, count=20)
    st2 = Stock(id=12, id_book=8, id_shop=4, count=5)
    sl = Sale(id=7, price=600, date_sale='2022-11-09', id_stock=10, count=5)
    sl1 = Sale(id=8, price=580, date_sale='2022-11-05', id_stock=11, count=10)

    session.add_all([pb, sh, sh1, bk, bk1, bk2, st, st1, st2, sl, sl1])
    session.commit()

    select_sale()

    session.close()
