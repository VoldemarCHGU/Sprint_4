from conftest import *


class TestBooksCollector:

    @pytest.mark.parametrize('books',
                             [
                                 {"books": ['Книга 1'], "waiting": {'Книга 1': ''}},
                                 {"books": ['Книга 1', 'Книга 2'], "waiting": {'Книга 1': '', 'Книга 2': ''}},
                                 {"books": ['Книга 1', 'Книга 2', 'Книга 1'],
                                  "waiting": {'Книга 1': '', 'Книга 2': ''}},
                                 {"books": ['Книга с длинным названием до 40 символов'],
                                  "waiting": {'Книга с длинным названием до 40 символов': ''}},
                                 {"books": ['Книга с длинным названием от 41 символа!!'], "waiting": {}}
                             ])
    def test_add_new_book(self, book_collector, books):
        for book in books['books']:
            book_collector.add_new_book(book)
        assert book_collector.get_books_genre() == books['waiting']

    @pytest.mark.parametrize('name,  waiting', [
        ['Книга 1', 'Ужасы'],
        ['Книга 2', ''],
        ['Книга 3', 'Детективы'],
        ['Книга 4', 'Ужасы'],
    ])
    def test_set_book_genre(self, create_test_data_book_collector, name, waiting):
        collector = create_test_data_book_collector
        assert collector.get_book_genre(name) == waiting

    @pytest.mark.parametrize('name, waiting', [
        ['Книга 1', ''],
    ])
    def test_get_book_genre_after_add_book(self, book_collector, name, waiting):
        collector = book_collector
        collector.add_new_book(name)
        assert collector.get_book_genre(name) == waiting

    @pytest.mark.parametrize('name, waiting', [
        ['Книга 1', 'Ужасы'],
        ['Книга 2', ''],
        ['Книга 3', 'Детективы'],
        ['Книга 4', 'Ужасы'],
    ])
    def test_get_book_genre_after_set_genre(self, create_test_data_book_collector, name, waiting):
        collector = create_test_data_book_collector
        assert collector.get_book_genre(name) == waiting

    @pytest.mark.parametrize('genre, waiting', [
        ['Ужасы', ['Книга 1', 'Книга 4']],
        ['Нет такого жанра', []],
        ['Детективы', ['Книга 3']],
        ['Комедии', []]
    ])
    def test_get_books_with_specific_genre(self, create_test_data_book_collector, genre, waiting):
        collector = create_test_data_book_collector
        assert collector.get_books_with_specific_genre(genre) == waiting

    def test_get_books_genre_empty_list(self, book_collector):
        assert book_collector.get_books_genre() == {}

    def test_get_books_genre_after_add_books(self, book_collector):
        book_collector.add_new_book('Книга 1')
        assert book_collector.get_books_genre() == {'Книга 1': ''}

    def test_get_books_genre_after_add_books_and_set_genre(self, create_test_data_book_collector):
        waiting = {
            'Книга 1': 'Ужасы',
            'Книга 2': '',
            'Книга 3': 'Детективы',
            'Книга 4': 'Ужасы',
            'Книга 6': 'Мультфильмы',
        }
        assert create_test_data_book_collector.get_books_genre() == waiting

    def test_get_books_for_children(self, create_test_data_book_collector):
        expected = ['Книга 6']  # 'Мультфильмы'
        assert create_test_data_book_collector.get_books_for_children() == expected

    @pytest.mark.parametrize('name, waiting', [
        ['Книга 3', ['Книга 3']],
        ['Нет такой книги', []]
    ])
    def test_add_book_in_favorites_first_try(self, create_test_data_book_collector, name, waiting):
        book_collector = create_test_data_book_collector
        book_collector.add_book_in_favorites(name)
        assert book_collector.get_list_of_favorites_books() == waiting

    @pytest.mark.parametrize('name, waiting', [
        ['Книга 3', ['Книга 3']],
        ['Нет такой книги', []]
    ])
    def test_add_book_in_favorites_second_try(self, create_test_data_book_collector, name, waiting):
        book_collector = create_test_data_book_collector
        book_collector.add_book_in_favorites(name)
        book_collector.add_book_in_favorites(name)  # Повторно пытаемся добавить
        assert book_collector.get_list_of_favorites_books() == waiting

    @pytest.mark.parametrize('name, delete_name, waiting', [
        ['Книга 3', 'Книга 3', []],
        ['Книга 3', 'Книга 1', ['Книга 3']],
    ])
    def test_delete_book_from_favorites(self, create_test_data_book_collector, name, delete_name, waiting):
        create_test_data_book_collector.add_book_in_favorites(name)
        create_test_data_book_collector.delete_book_from_favorites(delete_name)
        assert create_test_data_book_collector.get_list_of_favorites_books() == waiting

    def test_get_list_of_favorites_books_empty_list(self, book_collector):
        assert book_collector.get_list_of_favorites_books() == []
