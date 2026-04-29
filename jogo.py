class Jogo:
    def __init__(self, id_jogo, titulo, console, genero, publisher,
                 developer, critic_score, total_sales,
                 na_sales, jp_sales, pal_sales, other_sales, release_date):

        self.id = id_jogo
        self.titulo = titulo
        self.console = console
        self.genero = genero
        self.publisher = publisher
        self.developer = developer
        self.critic_score = critic_score
        self.total_sales = total_sales
        self.na_sales = na_sales
        self.jp_sales = jp_sales
        self.pal_sales = pal_sales
        self.other_sales = other_sales
        self.release_date = release_date

    def exibir(self):
        print(f'ID: {self.id}')
        print(f'Titulo: {self.titulo}')
        print(f'Console: {self.console}')
        print(f'Genero: {self.genero}')
        print(f'Publisher: {self.publisher}')
        print(f'Developer: {self.developer}')
        print(f'Nota da critica: {self.critic_score}')
        print(f'Vendas totais: {self.total_sales}')
        print(f'Vendas NA: {self.na_sales}')
        print(f'Vendas JP: {self.jp_sales}')
        print(f'Vendas PAL: {self.pal_sales}')
        print(f'Outras vendas: {self.other_sales}')
        print(f'Data de lancamento: {self.release_date}')
        print('-' * 60)

    def linha_backlog(self):
        titulo = self.titulo.replace(';', ',')
        console = self.console.replace(';', ',')
        return f'{self.id};{titulo};{console}'

    def linha_recente(self):
        titulo = self.titulo.replace(';', ',')
        console = self.console.replace(';', ',')
        return f'{self.id};{titulo};{console}'
