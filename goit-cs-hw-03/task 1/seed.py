import psycopg2
from random import randint
from faker import Faker

# ============================== Configuration ==============================
DB_NAME = "hw03_db"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = 5432

# ============================== Initialization ==============================
fake = Faker()
NUM_USERS = 10
NUM_TASKS = 30


# ============================== Main Logic ==================================
def seed():
    """Populate the PostgreSQL database with fake users and tasks.

    Generates random users and inserts them into the 'users' table,
    then creates tasks with random titles and descriptions, assigning
    them to the created users and linking to random statuses (1 to 3).
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Insert users
        user_ids = []
        for _ in range(NUM_USERS):
            full_name = fake.name()
            email = fake.unique.email()
            cursor.execute(
                """
                INSERT INTO users (fullname, email)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (full_name, email)
            )
            user_id = cursor.fetchone()[0]
            user_ids.append(user_id)

        # Insert tasks
        for _ in range(NUM_TASKS):
            title = fake.sentence(nb_words=5)
            description = fake.paragraph(nb_sentences=2)
            status_id = randint(1, 3)
            user_id = fake.random_element(user_ids)
            cursor.execute(
                """
                INSERT INTO tasks (title, description, status_id, user_id)
                VALUES (%s, %s, %s, %s);
                """,
                (title, description, status_id, user_id)
            )

        print("Seeding completed successfully.")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during seeding: {e}")


if __name__ == "__main__":
    seed()
