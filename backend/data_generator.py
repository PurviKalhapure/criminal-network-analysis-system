from faker import Faker
import random
import json

fake = Faker('en_IN')

def generate_dataset(num_people=150, num_events=400):
    people = []
    for i in range(num_people):
        people.append({
            "id": f"P{i}",
            "name": fake.name(),
            "phone": fake.phone_number(),
            "address": fake.address(),
            "risk_flag": random.choice([True, False, False, False, False])
        })

    relationships = []
    rel_types = ["CALLED", "TRANSFERRED_MONEY", "MET_AT", "FAMILY_OF", "ASSOCIATE_OF"]
    for _ in range(num_events):
        p1, p2 = random.sample(people, 2)
        relationships.append({
            "source": p1["id"],
            "target": p2["id"],
            "type": random.choice(rel_types),
            "timestamp": fake.date_time_this_year().isoformat(),
            "amount": random.randint(500, 500000) if random.random() > 0.5 else None,
            "location": fake.city()
        })

    return {"people": people, "relationships": relationships}

if __name__ == "__main__":
    data = generate_dataset()
    with open("synthetic_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generated {len(data['people'])} people, {len(data['relationships'])} relationships")