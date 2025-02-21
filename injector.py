import sqlalchemy as db

def injection(table):
    # connection = db.create_engine("postgresql://myuser:mypassword@localhost:5432/mydb")
    connection = db.create_engine("postgresql://neondb_owner:npg_FBvTi18ySpoY@ep-yellow-salad-a9lbdmij-pooler.gwc.azure.neon.tech/neondb?sslmode=require")
    table.to_sql(
        "prices",
        connection,
        index=False,
        if_exists="append",
        dtype={
            "price": db.Float()
        },
    )
