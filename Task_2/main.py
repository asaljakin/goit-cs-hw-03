import argparse

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

config = dotenv_values(".env")

uri = f"mongodb://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.cs03

parser = argparse.ArgumentParser(description="Add a new cat")
parser.add_argument("--action", help="[create, read, update-age, add-feature, delete]")
parser.add_argument("--id", help="ID of the cat")
parser.add_argument("--name", help="Name of the cat")
parser.add_argument("--age", help="Age of the cat")
parser.add_argument("--feature", help="Feature of the cat")
parser.add_argument("--features", help="Features of the cat", nargs="+")

args = parser.parse_args()
action = args.action
pk = args.id
name = args.name
age = args.age
feature = args.feature
features = args.features


def read(name=None):
    if name:
        return db.cats.find_one({"name": name})
    else:
        return db.cats.find()


def create(name, age, features):
    return db.cats.insert_one({
        "name": name,
        "age": age,
        "features": features
    })


def update_age(name, age):
    return db.cats.update_one(
        {
            "name": name
        },
        {
            "$set": {
                "age": age,
            }
        }
    )


def add_feature(name, feature):
    return db.cats.update_one(
        {
            "name": name
        },
        {
            "$push": {
                "features": feature
            }
        }
    )


def delete(name):
    if name:
        return db.cats.delete_one({"name": name})
    else:
        return db.cats.delete_many({})


if __name__ == "__main__":
    match action:
        case "read":
            if name:
                print(read(name))
            else:
                [print(cat) for cat in read()]
        case "create":
            if name is not None or age is not None or features is not None:
                r = create(name, age, features)
                print(r.inserted_id)
            else:
                print("Missing arguments for create '--name', '--age' and '--features'")
        case "update-age":
            if name is not None and age is not None:
                r = update_age(name, age)
                print(r.modified_count)
            else:
                print("Missing arguments for update-age '--name' and '--age'")
        case "add-feature":
            if feature is not None and name is not None:
                r = add_feature(name, feature)
                print(r.modified_count)
            else:
                print("Missing arguments for add-feature '--name' and '--feature'")
        case "delete":
            r = delete(name)
            print(r.deleted_count)
        case _:
            print("Unknown action")
