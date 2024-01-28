import pytest
from main import BooksCollector


@pytest.fixture
def book_collector():
    collector = BooksCollector()
    return collector


@pytest.fixture
def create_test_data_book_collector():
    """
    Для формирования тестового набора
        {
        'Книга 1': 'Ужасы',
        'Книга 2': '',
        'Книга 3': 'Детективы',
        'Книга 4': 'Ужасы',
        'Книга 6': 'Мультфильмы',
        }
    """
    collector = BooksCollector()
    test_data = [
        {'book': 'Книга 1', 'genre': 'Ужасы'},  # add
        {'book': 'Книга 2', 'genre': 'Нет такого жанра'},  # add, будет без жанра
        {'book': 'Книга 1', 'genre': 'Нет такого жанра'},  # not add, Книга 1 уже есть в списке
        {'book': 'Книга 3', 'genre': 'Детективы'},  # add
        {'book': 'Книга 4', 'genre': 'Ужасы'},  # add, ещё 1 жанр "Ужасы"
        {'book': 'Книга 5 с длинным названием > 41 символа!!', 'genre': 'Ужасы'},  # not add, длина не соответствует
        {'book': 'Книга 6', 'genre': 'Мультфильмы'},
    ]
    for data in test_data:
        collector.add_new_book(data['book'])
        collector.set_book_genre(data['book'], data['genre'])
    return collector
