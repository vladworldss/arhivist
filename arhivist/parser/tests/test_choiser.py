from arhivist.api.choiser import Choiser

resps = [
    {"title": "J.K.Roling. Harry Potter and the Philosopher's Stone some_text"},
    {"title": "J.K.Roling. Harry Potter and the Philosopher's Stone"},  # best
    {"title": "01 Harry Potter and the Goblet of Fire"},
    {"title": "Full Complete story: Harry Potter"},
]


def test_best_choise():
    title = "01 J K Roling. Harry Potter and the Philosopher's Stone"
    best = Choiser.best_choise(value=title, choises=resps, field="title")
    assert best == resps[1]

def test_best_book_choise():
    title = "01 J K Roling. Harry Potter and the Philosopher's Stone"
    best = Choiser.best_book_choise(value=title, choises=resps)
    assert best == resps[1]
