import pytest

from arhivist.parser.item import Book


@pytest.mark.parametrize(
    "title,result", [
        ("Harry Potter and the Philosopher's Stone.pdf", ("Harry Potter and the Philosopher's Stone", "pdf")),
        ("Harry Potter and the Chamber of Secrets.djvu", ("Harry Potter and the Chamber of Secrets", "djvu")),
        ("Гарри Поттер и Узник Азкабана.djv", ("Гарри Поттер и Узник Азкабана", "djv")),
        ("01 Harry Potter and the Goblet of Fire.epub", ("01 Harry Potter and the Goblet of Fire", "epub")),
        ("Harry_Potter_and_the_Order of the Phoenix.fb2", ("Harry_Potter_and_the_Order of the Phoenix", "fb2")),
        ("Harry Potter and the Half-Blood Prince.avi", None),
        ("__Harry Potter and the Deathly Hallows.mp3", None)
    ]
)
def test_match_title(title, result):
    m = Book.match(title)
    assert  m == result


def test_to_json():
    kw = ["Harry Potter and the Philosopher's Stone",
          "/home/books/Harry Potter and the Philosopher's Stone.pdf",
          "pdf"
          ]
    b = Book(*kw)
    json_book = b.to_json()
    assert all([x in json_book for x in kw ])

def test_from_json():
    pass

def test_get_meta():
    pass

def test_update():
    b = Book("Harry Potter and the Philosopher's Stone.pdf", "Harry Potter and the Philosopher's Stone", "pdf")
    json_str = '{"publisher": "OREALLY", "category": "FICTION"}'
    b.update(json_str)
    assert b.publisher == "OREALLY"
    assert b.category == "FICTION"
    with pytest.raises(AttributeError):
        bad_json_str = '{"bad_param": "REALLY_BAD"}'
        b.update(bad_json_str)




def test_dict():
    class DictWatch(dict):
        def __init__(self, *args, **kwargs):
            self.update(*args, **kwargs)
            self.__x = None

        @property
        def x(self):
            return dict.__getitem__(self, self.__x)

        @x.setter
        def x(self, val):
            dict.__setitem__(self, "x", val)

        def __getitem__(self, key):
            val = dict.__getitem__(self, key)
            return val

        def __setitem__(self, key, val):
            dict.__setitem__(self, key, val)

        def __repr__(self):
            dictrepr = dict.__repr__(self)
            return '%s(%s)' % (type(self).__name__, dictrepr)

        def update(self, *args, **kwargs):
            for k, v in dict(*args, **kwargs).items():
                self[k] = v


    d = DictWatch()
    d.x = "X"
    vals = d.values()
    len(vals)
    d["z"] = "Z"
    len(vals)