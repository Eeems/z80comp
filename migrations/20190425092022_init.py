"""
Initial migration

name: init
version: 20190425092022
"""
import json


def upgrade(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS "tokens" (
            "name" TEXT PRIMARY KEY,
            "code" TEXT NOT NULL,
            "sizescore" INTEGER NOT NULL,
            "speedscore" INTEGER NOT NULL,
            "type" TEXT NOT NULL,
            "precedence" INTEGER NOT NULL,
            "numargs" INTEGER NOT NULL,
            "bytecode" TEXT
        )
    """)
    connection.execute("""
        CREATE INDEX IF NOT EXISTS "tokens_type" ON "tokens" ("type")
    """)
    with open('migrations/tokens.json', 'r') as f:
        data = json.load(f)

    for row in data:
        connection.execute("""
            INSERT INTO "tokens" VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        """, [
            row["name"], row["code"], row["sizescore"], row["speedscore"],
            row["type"], row["precedence"], row["numargs"], row["bytecode"]
        ])

    connection.commit()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS "z80" (
            "ir"    TEXT NOT NULL,
            "code"  TEXT NOT NULL,
            "size"  INTEGER NOT NULL,
            "speed" INTEGER NOT NULL,
            "input" TEXT NOT NULL,
            "output"    TEXT NOT NULL,
            "requires"  TEXT NOT NULL DEFAULT '',
            "state" TEXT NOT NULL,
            "destroys"  TEXT NOT NULL
        )
    """)
    with open('migrations/z80.json', 'r') as f:
        data = json.load(f)

    for row in data:
        connection.execute("""
            INSERT INTO "z80" VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
        """, [
            row["ir"], row["code"], row["size"], row["speed"], row["input"],
            row["output"], row["requires"], row["state"], row["destroys"]
        ])

    connection.commit()


def downgrade(connection):
    connection.execute("""
        DROP TABLE tokens
    """)
    connection.execute("""
        DROP TABLE z80
    """)
