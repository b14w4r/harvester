import sqlalchemy as db

def injection(table):
    connection = db.create_engine("postgresql://myuser:mypassword@localhost:5432/mydb")
    table.to_sql(
        "prices",
        connection,
        index=False,
        if_exists="append",
        dtype={
            "price": db.Float()
        },
    )
