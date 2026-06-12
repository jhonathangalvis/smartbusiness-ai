from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres:jhonathan84@127.0.0.1:5432/smartbusiness_db"

try:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database();")
        )

        print("Conexión exitosa")
        print("Base de datos:", result.scalar())

except Exception as e:
    print("ERROR:")
    print(type(e))
    print(e)