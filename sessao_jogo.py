from datetime import datetime


class SessaoJogo:
    def __init__(self, jogo, tempo_jogado, tempo_total=0.0, data_sessao=''):
        self.jogo = jogo
        self.tempo_jogado = tempo_jogado
        self.tempo_total = tempo_total

        if data_sessao == '':
            self.data_sessao = datetime.now().strftime('%Y-%m-%d')
        else:
            self.data_sessao = data_sessao

        self.status = self.definir_status()

    def definir_status(self):
        if self.tempo_total < 2:
            return 'iniciado'
        if self.tempo_total < 10:
            return 'em andamento'
        if self.tempo_total < 20:
            return 'muito jogado'
        return 'concluído simbolicamente'

    def exibir(self):
        print(f'Jogo: {self.jogo.titulo}')
        print(f'Tempo da sessao: {self.tempo_jogado:.2f} horas')
        print(f'Tempo total: {self.tempo_total:.2f} horas')
        print(f'Data: {self.data_sessao}')
        print(f'Status: {self.status}')
        print('-' * 60)

    def linha_historico(self):
        titulo = self.jogo.titulo.replace(';', ',')
        return (f'{self.jogo.id};{titulo};{self.tempo_jogado:.2f};'
                f'{self.tempo_total:.2f};{self.data_sessao};{self.status}')
