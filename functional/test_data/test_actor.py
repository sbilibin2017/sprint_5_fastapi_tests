import random
import uuid

from conftest import test_settings


def es_generate_actor_data() -> list[dict]:
    rnd = random.Random()
    data = []
    for _ in range(test_settings.ELASTIC_SAMPLE_SIZE):
        rnd.seed(test_settings.SEED + _ + 1)
        random_uuid = uuid.UUID(int=rnd.getrandbits(128), version=4)
        row = {
            "id": str(random_uuid),
            "full_name": "Robert Polson",
            "film": [
                {
                    "id": "55c723c1-6d90-4a04-a44b-e9792040251a"
                },
                {
                    "id": "9c91a5b2-eb70-4889-8581-ebe427370edd"
                }
            ]
        }
        data.append(row)
    return data
