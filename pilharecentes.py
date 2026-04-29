class PilhaRecentes:
    def __init__(self, limite=20):
        self.dados = []
        self.limite = limite

    def push(self, jogo):
        indice = -1

        for i in range(len(self.dados)):
            if self.dados[i].id == jogo.id:
                indice = i
                break

        if indice != -1:
            self.dados.pop(indice)

        self.dados.append(jogo)

        if len(self.dados) > self.limite:
            self.dados.pop(0)

    def pop(self):
        if self.is_empty():
            return None
        return self.dados.pop()

    def topo(self):
        if self.is_empty():
            return None
        return self.dados[-1]

    def is_empty(self):
        return len(self.dados) == 0

    def tamanho(self):
        return len(self.dados)

    def mostrar(self):
        if self.is_empty():
            print('Nenhum jogo recente.')
            return

        print('Jogos recentes:')
        for indice, jogo in enumerate(reversed(self.dados), start=1):
            print(f'{indice}. ID {jogo.id} - {jogo.titulo} ({jogo.console})')
