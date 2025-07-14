from pymongo import MongoClient
from pymongo.server_api import ServerApi


# ============================== DB SETUP ==============================
client = MongoClient("mongodb://user:password@localhost:27017", server_api=ServerApi("1"))
db = client["cats_db"]
collection = db["cats"]


# ============================== CREATE ==============================
def create_cat(name, age, features):
    """Insert a new cat document."""
    try:
        result = collection.insert_one({
            "name": name,
            "age": age,
            "features": features
        })
        print(f"Inserted: {result.inserted_id}")
    except Exception as e:
        print("Error during insert:", e)


# ============================== READ ==============================
def read_all_cats():
    """Read and print all cats."""
    try:
        for cat in collection.find():
            print(cat)
    except Exception as e:
        print("Error during reading:", e)


def read_cat_by_name(name):
    """Find cat by name."""
    try:
        cat = collection.find_one({"name": name})
        print(cat if cat else "Cat not found.")
    except Exception as e:
        print("Error during lookup:", e)


# ============================== UPDATE ==============================
def update_cat_age(name, new_age):
    """Update cat's age by name."""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        print("Age updated." if result.modified_count else "No update.")
    except Exception as e:
        print("Error during age update:", e)


def add_feature(name, feature):
    """Add feature to cat."""
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
        print("Feature added." if result.modified_count else "No update.")
    except Exception as e:
        print("Error during feature update:", e)


# ============================== DELETE ==============================
def delete_cat(name):
    """Delete one cat by name."""
    try:
        result = collection.delete_one({"name": name})
        print("Deleted." if result.deleted_count else "Not found.")
    except Exception as e:
        print("Error during delete:", e)


def delete_all_cats():
    """Delete all cats."""
    try:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} cats.")
    except Exception as e:
        print("Error during full delete:", e)


# ============================== EXAMPLE USAGE ==============================
if __name__ == "__main__":
    # Optional: clean the collection before seeding
    delete_all_cats()

    print("\nCreating 10 cats...")
    create_cat("Whiskers", 2, ["likes milk", "sleeps on laptop", "chases flies"])
    create_cat("Mittens", 4, ["purrs loudly", "hides in boxes", "loves tuna"])
    create_cat("Shadow", 3, ["nocturnal", "black fur", "silent walker"])
    create_cat("Luna", 1, ["jumps high", "plays with string", "meows constantly"])
    create_cat("Simba", 5, ["brave", "likes to climb", "roars"])
    create_cat("Oliver", 6, ["cuddly", "sits on keyboard", "loves belly rubs"])
    create_cat("Cleo", 3, ["friendly", "hates vacuum", "licks windows"])
    create_cat("Toby", 2, ["scratches furniture", "loves naps", "steals socks"])
    create_cat("Nala", 4, ["protective", "chases birds", "watches TV"])
    create_cat("Leo", 7, ["king of the house", "eats everything", "chill"])

    print("\nReading all cats:")
    read_all_cats()

    print("\nReading one cat by name: 'Simba'")
    read_cat_by_name("Simba")

    print("\nUpdating 'Simba' age to 6")
    update_cat_age("Simba", 6)
    read_cat_by_name("Simba")

    print("\nAdding new feature to 'Simba': 'scratches curtains'")
    add_feature("Simba", "scratches curtains")
    read_cat_by_name("Simba")

    print("\nDeleting one cat: 'Toby'")
    delete_cat("Toby")
    read_cat_by_name("Toby")

    print("\nFinal list of cats:")
    read_all_cats()
