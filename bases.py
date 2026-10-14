import sqlite3

base = sqlite3.connect("table.db")
cursore = base.cursor()

message = '''INSERT INTO card_to_user(id_card, name_user, time)
         VALUES ('04A31B5F2C80', 'Андрей', '2026-10-14 20:00:00')'''

cursore.execute(message)
base.commit()
cursore.close()
base.close()