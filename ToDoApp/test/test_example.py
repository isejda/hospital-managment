import pytest


def test_equal_or_not_equal():
    assert 3==3
    assert 3!=2

def test_is_instance():
    assert isinstance('string', str)
    assert not isinstance(10, str)

def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_types():
    assert type('string' is str)
    assert type('string' is not int)
    assert type('string') == str

def test_grater_and_less_than():
    assert 3>2
    assert 1<2

def test_list():
    num_list = [1,2,3]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.year = year

@pytest.fixture
def student():
    return Student('John', 'Smith', 'Computer Science', 3)

def test_person_initialization():
    p = Student('John', 'Smith', 'Computer Science', 3)
    assert p.first_name == 'John', 'First name should be John'
    assert p.last_name == 'Smith', 'Last name should be Smith'
    assert p.major == 'Computer Science', 'Major should be Computer Science'
    assert p.year == 3, 'Year should be 3'

def test_person_initialization2(student):
    assert student.first_name == 'John', 'First name should be John'
    assert student.last_name == 'Smith', 'Last name should be Smith'
    assert student.major == 'Computer Science', 'Major should be Computer Science'
    assert student.year == 3, 'Year should be 3'