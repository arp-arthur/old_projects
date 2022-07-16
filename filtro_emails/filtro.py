from db.Database import Database


class Filtro:
    def filter_emails(self, palavras_in, palavras_out, aplica_filtros_in, aplica_filtros_out, grava_base=False, filtra_presuf_in=False):
        self.emails_filtrados = []
        palavras_in_list = palavras_in.split(';')
        palavras_out_list = palavras_out.split(';')
        print(aplica_filtros_in)
        print(aplica_filtros_out)

        with open('emails.txt', 'r', encoding='utf-8') as emails_file:
            if aplica_filtros_in and palavras_in != '':
                for email in emails_file.readlines():
                    for palavra_in in palavras_in_list:
                        if filtra_presuf_in:
                            if palavra_in[:3] in email and email not in self.emails_filtrados:
                                self.emails_filtrados.append(email)
                        else:
                            if palavra_in in email and email not in self.emails_filtrados:
                                self.emails_filtrados.append(email)
            else:
                self.emails_filtrados = emails_file.readlines()

            if aplica_filtros_out and palavras_out != '':
                for email in self.emails_filtrados:
                    for palavra_out in palavras_out_list:
                        if email in self.emails_filtrados and palavra_out in email:
                            self.emails_filtrados.remove(email)

            if grava_base:
                self.grava_database()

            self.save_file()

    def save_file(self,):
        with open('emails_filtrados.txt', 'w', encoding='utf-8') as emails_saida:
            for email in self.emails_filtrados:
                emails_saida.write(email)

    def grava_database(self,):
        db = Database()
        db.connect()
        db.create_table()
        db.insert_email(self.emails_filtrados)