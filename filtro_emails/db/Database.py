import sqlite3

class Database():

    def __init__(self):
        self.consulta_tabela_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='emails_filtrados'"
        self.crud_create_table = "CREATE TABLE IF NOT EXISTS emails_filtrados('emails')"

    def connect(self):
        print('realizando conexão')
        try:
            self.conn = sqlite3.connect('filtro_emails.db')
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    def create_table(self):
        print('criando tabela')
        try:
            if self.cur.execute(self.consulta_tabela_exists).fetchall() == []:
                self.cur.execute(self.crud_create_table)
                self.conn.commit()
        except Exception as e:
            print(e)

    def get_all_emails(self):
        return self.cur.execute('SELECT * FROM emails_filtrados').fetchall()

    def insert_email(self, emails_list):
        print('gravando registros')
        for email in emails_list:
            self.cur.execute('INSERT INTO emails_filtrados(emails) VALUES (?)', email)
        self.conn.commit()