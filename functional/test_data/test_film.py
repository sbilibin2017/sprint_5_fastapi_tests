import random
import uuid

from conftest import test_settings


def es_generate_film_data() -> list[dict]:
    rnd = random.Random()
    data = []
    for _ in range(test_settings.ELASTIC_SAMPLE_SIZE):
        rnd.seed(test_settings.SEED + _ + 6)
        random_uuid = uuid.UUID(int=rnd.getrandbits(128), version=4)
        row = {
            "id": str(random_uuid),
            "title": "The Star",
            "imdb_rating": random.uniform(0, 10),
            "type": "movie",
            "creation_date": None,
            "description": None,
            "genre__name": [
                "Family",
                "Musical"
            ],
            "director__full_name": [],
            "writer__full_name": [],
            "actor__full_name": [
                "Lori Alan",
                "Jason Dolley",
                "John D'Aquino",
                "Lisa Arch"
            ],
            "genre": [
                {
                    "id": "55c723c1-6d90-4a04-a44b-e9792040251a",
                    "name": "Family"
                },
                {
                    "id": "9c91a5b2-eb70-4889-8581-ebe427370edd",
                    "name": "Musical"
                }
            ],
            "director": [],
            "writer": [],
            "actor": [
                {
                    "id": "99cb58d0-4b03-46ce-b581-d9d9887a97c2",
                    "full_name": "Lori Alan"
                },
                {
                    "id": "1db6d260-e8dd-46e9-b610-6609dcf04231",
                    "full_name": "Jason Dolley"
                },
                {
                    "id": "9cefe2b3-cf3c-4c3f-be22-554604cd6146",
                    "full_name": "John D'Aquino"
                },
                {
                    "id": "7ae6bfd2-3fab-4b8a-9e08-f2c901bf1869",
                    "full_name": "Lisa Arch"
                }
            ]
        }
        data.append(row)
    return data
