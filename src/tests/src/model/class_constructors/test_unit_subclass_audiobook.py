from src.model.class_constructors.subclass_audiobook import Audiobook
from faker import Faker

fake = Faker()

def test_audiobook():
    fake_title = fake.text()
    audiobook = Audiobook(fake_title)
    assert audiobook.title == fake_title