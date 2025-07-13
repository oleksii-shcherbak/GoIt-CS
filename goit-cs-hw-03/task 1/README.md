## Setup
1. Start PostgreSQL using Docker or your local instance.
2. Execute `init.sql` to create all required tables and insert base status data.
3. Install dependencies by running: `pip install -r requirements.txt`
(This will install `faker` and `psycopg2-binary`)
4. Run `seed.py` to populate the database with fake users and tasks.
5. Open and run this `queries.sql` file step by step in your SQL tool.
