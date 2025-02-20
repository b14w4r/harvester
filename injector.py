import pandas as pd
import sqlalchemy as db


csv_file = pd.read_csv("data.csv")


def injection(csv_file) :
    connection = db.create_engine("postgresql://myuser:mypassword@localhost:5432/mydb")
    csv_file.to_sql(
        "HRDB",
        connection,
        index=False,
        if_exists="replace",
        dtype={
            "Name": db.VARCHAR(255),
            "City": db.VARCHAR(255),
            "Age": db.Integer(),
        },
    )


injection(csv_file)
