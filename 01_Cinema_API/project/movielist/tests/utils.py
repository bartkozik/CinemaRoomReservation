from random import sample, randint, choice
from faker import Faker

from movielist.models import Person, Movie


faker = Faker("pl_PL")


def random_person():
    """Return a random Person object from db."""
    people = Person.objects.all()
    return choice(people)


def fake_movie_data():
    """Generate a dict of movie data

    The format is compatible with serializers (`Person` relations
    represented by names).
    """
    movie_data = {
        "title": f"{faker.job()} {faker.first_name()}",
        "description": faker.sentence(),
        "year": int(faker.year()),
        "director": random_person().name,
    }
    people = Person.objects.all()
    actors = sample(list(people), randint(1, len(people)))
    actor_names = [a.name for a in actors]
    movie_data["actors"] = actor_names
    return movie_data


def find_person_by_name(name):
    """Return the first `Person` object that matches `name`."""
    return Person.objects.filter(name=name).first()


def create_fake_movie():
    """Generate new fake movie and save to database."""
    movie_data = fake_movie_data()
    movie_data["director"] = find_person_by_name(movie_data["director"])
    actors = movie_data["actors"]
    del movie_data["actors"]
    new_movie = Movie.objects.create(**movie_data)
    for actor in actors:
        new_movie.actors.add(find_person_by_name(actor))

