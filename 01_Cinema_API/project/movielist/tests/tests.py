import pytest

from movielist.models import Movie, Person
from .utils import fake_movie_data, random_person


@pytest.mark.django_db
def test_post_movie(client, set_up):
    movies_before = Movie.objects.count()
    new_movie = fake_movie_data()
    response = client.post("/movies/", new_movie, format='json')
    assert response.status_code == 201
    assert Movie.objects.count() == movies_before + 1
    for key, value in new_movie.items():
        assert key in response.data
        if isinstance(value, list):
            # Compare contents regardless of their order
            assert len(response.data[key]) == len(value)
        else:
            assert response.data[key] == value


@pytest.mark.django_db
def test_get_movie_list(client, set_up):
    response = client.get("/movies/", {}, format='json')

    assert response.status_code == 200
    assert Movie.objects.count() == len(response.data)


@pytest.mark.django_db
def test_get_movie_detail(client, set_up):
    movie = Movie.objects.first()
    response = client.get(f"/movies/{movie.id}/", {}, format='json')

    assert response.status_code == 200
    for field in ("title", "year", "description", "director", "actors"):
        assert field in response.data


@pytest.mark.django_db
def test_delete_movie(client, set_up):
    movie = Movie.objects.first()
    response = client.delete(f"/movies/{movie.id}/", {}, format='json')
    assert response.status_code == 204
    movie_ids = [movie.id for movie in Movie.objects.all()]
    assert movie.id not in movie_ids


@pytest.mark.django_db
def test_update_movie(client, set_up):
    movie = Movie.objects.first()
    response = client.get(f"/movies/{movie.id}/", {}, format='json')
    movie_data = response.data
    new_year = 3
    movie_data["year"] = new_year
    new_actors = [random_person().name]
    movie_data["actors"] = new_actors
    response = client.patch(f"/movies/{movie.id}/", movie_data, format='json')
    assert response.status_code == 200
    movie_obj = Movie.objects.get(id=movie.id)
    assert movie_obj.year == new_year
    db_actor_names = [actor.name for actor in movie_obj.actors.all()]
    assert len(db_actor_names) == len(new_actors)
