from databases import Database

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/mydatabase"
database = Database(DATABASE_URL)

