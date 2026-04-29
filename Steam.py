import csv
import os

from filabacklog import FilaBacklog
from jogo import Jogo
from pilharecentes import PilhaRecentes
from sessao_jogo import SessaoJogo


class SteamPy:
    def __init__(self):
        self.catalogo = []
        self.jogos_por_id = {}
        self.backlog = FilaBacklog()
        self.recentes = PilhaRecentes()
        self.historico = []
        self.tempos_por_jogo = {}
        self.arquivo_dataset = 'dataset.csv'
        self.arquivo_backlog = 'backlog.txt'
        self.arquivo_historico = 'historico_jogo.txt'
        self.arquivo_recentes = 'recentes.txt'

    def caminho_local(self, nome_arquivo):
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(pasta_atual, nome_arquivo)

    def converter_float(self, valor):
        if valor is None:
            return 0.0

        valor = str(valor).strip().replace(',', '.')
        if valor == '':
            return 0.0

        try:
            return float(valor)
        except ValueError:
            return 0.0

    def carregar_jogos(self, nome_arquivo):
        caminho = nome_arquivo
        if not os.path.exists(caminho):
            caminho = self.caminho_local(nome_arquivo)

        if not os.path.exists(caminho):
            print(f'Arquivo {nome_arquivo} nao encontrado.')
            return

        self.arquivo_dataset = nome_arquivo
        self.catalogo = []
        self.jogos_por_id = {}
        total_linhas_invalidas = 0

        try:
            with open(caminho, 'r', encoding='utf-8', errors='replace',
                      newline='') as arquivo:
                leitor = csv.reader(arquivo)
                next(leitor, None)
                proximo_id = 1

                for linha in leitor:
                    if len(linha) < 14:
                        total_linhas_invalidas += 1
                        continue

                    titulo = linha[1].strip()
                    if titulo == '':
                        total_linhas_invalidas += 1
                        continue

                    jogo = Jogo(
                        proximo_id,
                        titulo,
                        linha[2].strip(),
                        linha[3].strip(),
                        linha[4].strip(),
                        linha[5].strip(),
                        self.converter_float(linha[6]),
                        self.converter_float(linha[7]),
                        self.converter_float(linha[8]),
                        self.converter_float(linha[9]),
                        self.converter_float(linha[10]),
                        self.converter_float(linha[11]),
                        linha[12].strip()
                    )

                    self.catalogo.append(jogo)
                    self.jogos_por_id[jogo.id] = jogo
                    proximo_id += 1

            print(f'Catalogo carregado com {len(self.catalogo)} jogos.')
            if total_linhas_invalidas > 0:
                print(f'Linhas invalidas ignoradas: {total_linhas_invalidas}')
        except OSError:
            print('Erro ao abrir o dataset.')

    def carregar_backlog(self):
        self.backlog = FilaBacklog()
        caminho = self.caminho_local(self.arquivo_backlog)

        if not os.path.exists(caminho):
            return

        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    partes = linha.strip().split(';')
                    if len(partes) < 1:
                        continue

                    try:
                        id_jogo = int(partes[0])
                    except ValueError:
                        continue

                    jogo = self.jogos_por_id.get(id_jogo)
                    if jogo is not None:
                        self.backlog.enqueue(jogo)

            print(f'Backlog carregado com {self.backlog.tamanho()} jogos.')
        except OSError:
            print('Nao foi possivel carregar o backlog.')

    def salvar_backlog(self):
        caminho = self.caminho_local(self.arquivo_backlog)

        try:
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                for jogo in self.backlog.dados:
                    arquivo.write(jogo.linha_backlog() + '\n')
            print('Backlog salvo.')
        except OSError:
            print('Nao foi possivel salvar o backlog.')

    def carregar_historico(self):
        self.historico = []
        self.tempos_por_jogo = {}
        self.recentes = PilhaRecentes()
        caminho = self.caminho_local(self.arquivo_historico)

        if not os.path.exists(caminho):
            return

        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    partes = linha.strip().split(';')
                    if len(partes) < 6:
                        continue

                    try:
                        id_jogo = int(partes[0])
                    except ValueError:
                        continue

                    jogo = self.jogos_por_id.get(id_jogo)
                    if jogo is None:
                        continue

                    tempo_sessao = self.converter_float(partes[2])
                    tempo_total = self.converter_float(partes[3])
                    data_sessao = partes[4]
                    status = partes[5]

                    sessao = SessaoJogo(jogo, tempo_sessao, tempo_total,
                                        data_sessao)
                    sessao.status = status
                    self.historico.append(sessao)
                    self.tempos_por_jogo[id_jogo] = tempo_total
                    self.recentes.push(jogo)

            print(f'Historico carregado com {len(self.historico)} sessoes.')
        except OSError:
            print('Nao foi possivel carregar o historico.')

    def salvar_historico(self):
        caminho = self.caminho_local(self.arquivo_historico)

        try:
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                for sessao in self.historico:
                    arquivo.write(sessao.linha_historico() + '\n')
            print('Historico salvo.')
        except OSError:
            print('Nao foi possivel salvar o historico.')

    def carregar_recentes(self):
        caminho = self.caminho_local(self.arquivo_recentes)

        if not os.path.exists(caminho):
            return

        recentes_carregados = PilhaRecentes()

        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    partes = linha.strip().split(';')
                    if len(partes) < 1:
                        continue

                    try:
                        id_jogo = int(partes[0])
                    except ValueError:
                        continue

                    jogo = self.jogos_por_id.get(id_jogo)
                    if jogo is not None:
                        recentes_carregados.push(jogo)

            self.recentes = recentes_carregados
            print(f'Recentes carregados com {self.recentes.tamanho()} jogos.')
        except OSError:
            print('Nao foi possivel carregar os jogos recentes.')

    def salvar_recentes(self):
        caminho = self.caminho_local(self.arquivo_recentes)

        try:
            with open(caminho, 'w', encoding='utf-8') as arquivo:
                for jogo in self.recentes.dados:
                    arquivo.write(jogo.linha_recente() + '\n')
            print('Recentes salvos.')
        except OSError:
            print('Nao foi possivel salvar os jogos recentes.')

    def mostrar_resultados(self, resultados, limite=20):
        if len(resultados) == 0:
            print('Nenhum jogo encontrado.')
            return

        print(f'{len(resultados)} resultado(s) encontrado(s).')
        print(f'Mostrando no maximo {limite} jogo(s):')
        print('-' * 60)

        for jogo in resultados[:limite]:
            print(f'ID {jogo.id} - {jogo.titulo} | {jogo.console} | '
                  f'{jogo.genero} | Nota {jogo.critic_score} | '
                  f'Vendas {jogo.total_sales}')

        print('-' * 60)

    def listar_jogos(self):
        self.mostrar_resultados(self.catalogo)

    def ler_id_jogo(self):
        valor = input('Digite o ID do jogo: ').strip()
        try:
            return int(valor)
        except ValueError:
            print('ID invalido.')
            return None

    def buscar_jogo_por_id(self):
        id_jogo = self.ler_id_jogo()
        if id_jogo is None:
            return None

        jogo = self.jogos_por_id.get(id_jogo)
        if jogo is None:
            print('Jogo nao encontrado.')
            return None

        return jogo

    def buscar_jogo_por_nome(self, termo):
        termo = termo.strip().lower()
        resultados = []

        for jogo in self.catalogo:
            if termo in jogo.titulo.lower():
                resultados.append(jogo)

        return resultados

    def buscar_por_nome(self):
        termo = input('Digite parte do nome do jogo: ')
        if termo.strip() == '':
            print('Termo de busca invalido.')
            return

        resultados = self.buscar_jogo_por_nome(termo)
        self.mostrar_resultados(resultados)

    def filtrar_por_genero(self, genero=None):
        if genero is None:
            genero = input('Digite o genero: ')

        genero = genero.strip().lower()
        if genero == '':
            print('Genero invalido.')
            return

        resultados = []

        for jogo in self.catalogo:
            if jogo.genero.lower() == genero:
                resultados.append(jogo)

        self.mostrar_resultados(resultados)

    def filtrar_por_console(self, console=None):
        if console is None:
            console = input('Digite o console: ')

        console = console.strip().lower()
        if console == '':
            print('Console invalido.')
            return

        resultados = []

        for jogo in self.catalogo:
            if jogo.console.lower() == console:
                resultados.append(jogo)

        self.mostrar_resultados(resultados)

    def filtrar_por_publisher(self, publisher=None):
        if publisher is None:
            publisher = input('Digite a publisher: ')

        publisher = publisher.strip().lower()
        if publisher == '':
            print('Publisher invalida.')
            return

        resultados = []

        for jogo in self.catalogo:
            if publisher in jogo.publisher.lower():
                resultados.append(jogo)

        self.mostrar_resultados(resultados)

    def filtrar_por_ano(self):
        ano = input('Digite o ano de lancamento: ').strip()

        if ano == '' or not ano.isdigit() or len(ano) != 4:
            print('Ano invalido.')
            return

        resultados = []

        for jogo in self.catalogo:
            data = jogo.release_date.strip()
            if data.startswith(ano) or ano in data:
                resultados.append(jogo)

        self.mostrar_resultados(resultados, limite=20)

    def filtrar_por_nota(self, nota_minima):
        nota_minima = self.converter_float(str(nota_minima))
        resultados = []

        for jogo in self.catalogo:
            if jogo.critic_score >= nota_minima:
                resultados.append(jogo)

        return resultados

    def filtrar_por_nota_minima(self):
        valor = input('Digite a nota minima: ')
        if valor.strip() == '':
            print('Nota invalida.')
            return

        nota_minima = self.converter_float(valor)
        resultados = self.filtrar_por_nota(nota_minima)

        self.mostrar_resultados(resultados)

    def filtrar_por_vendas_minimas(self):
        valor = input('Digite as vendas minimas: ')
        if valor.strip() == '':
            print('Vendas invalidas.')
            return

        vendas_minimas = self.converter_float(valor)
        resultados = []

        for jogo in self.catalogo:
            if jogo.total_sales >= vendas_minimas:
                resultados.append(jogo)

        self.mostrar_resultados(resultados)

    def ordenar_jogos(self, criterio):
        criterio = str(criterio).strip().lower()

        if criterio in ['1', 'titulo', 'título']:
            return sorted(self.catalogo, key=lambda jogo: jogo.titulo)
        if criterio in ['2', 'nota', 'critic_score']:
            return sorted(self.catalogo, key=lambda jogo: jogo.critic_score,
                          reverse=True)
        if criterio in ['3', 'vendas', 'vendas totais', 'total_sales']:
            return sorted(self.catalogo, key=lambda jogo: jogo.total_sales,
                          reverse=True)
        if criterio in ['4', 'data', 'data de lancamento',
                        'data de lançamento', 'release_date']:
            return sorted(self.catalogo, key=lambda jogo: jogo.release_date)
        if criterio in ['5', 'console']:
            return sorted(self.catalogo, key=lambda jogo: jogo.console)
        if criterio in ['6', 'genero', 'gênero']:
            return sorted(self.catalogo, key=lambda jogo: jogo.genero)

        return None

    def ordenar_catalogo(self):
        print('Criterios:')
        print('1. titulo')
        print('2. nota')
        print('3. vendas totais')
        print('4. data de lancamento')
        print('5. console')
        print('6. genero')
        opcao = input('Escolha uma opcao: ').strip()
        resultados = self.ordenar_jogos(opcao)

        if resultados is None:
            print('Opcao invalida.')
            return

        self.mostrar_resultados(resultados)

    def ids_no_backlog(self):
        ids = {}
        for jogo in self.backlog.dados:
            ids[jogo.id] = True
        return ids

    def adicionar_ao_backlog(self, jogo=None):
        if jogo is None:
            jogo = self.buscar_jogo_por_id()

        if jogo is None:
            return

        ids = self.ids_no_backlog()
        if jogo.id in ids:
            print('Esse jogo ja esta no backlog.')
            return

        self.backlog.enqueue(jogo)
        print(f'{jogo.titulo} adicionado ao backlog.')
        self.salvar_backlog()

    def jogar_proximo_backlog(self):
        if self.backlog.is_empty():
            print('Backlog vazio.')
            return

        jogo = self.backlog.dequeue()
        print(f'Proximo jogo do backlog: {jogo.titulo}')
        registrou = self.registrar_sessao(jogo)

        if registrou:
            self.salvar_backlog()
            self.salvar_historico()
            self.salvar_recentes()
        else:
            self.backlog.dados.insert(0, jogo)
            print('Sessao cancelada. O jogo voltou para o inicio do backlog.')

    def mostrar_backlog(self):
        self.backlog.mostrar()

    def mostrar_recentes(self):
        self.recentes.mostrar()

    def retomar_ultimo_jogo(self):
        jogo = self.recentes.topo()
        if jogo is None:
            print('Nenhum jogo recente para retomar.')
            return

        print(f'Retomando: {jogo.titulo}')
        registrou = self.registrar_sessao(jogo)
        if registrou:
            self.salvar_historico()
            self.salvar_recentes()

    def registrar_sessao(self, jogo, tempo=None):
        if tempo is None:
            valor = input('Quantas horas jogou nesta sessao? ').strip()
            tempo = self.converter_float(valor)
        else:
            tempo = self.converter_float(str(tempo))

        if tempo <= 0:
            print('O tempo precisa ser maior que zero.')
            return False

        tempo_total = self.tempos_por_jogo.get(jogo.id, 0.0) + tempo
        self.tempos_por_jogo[jogo.id] = tempo_total

        sessao = SessaoJogo(jogo, tempo, tempo_total)
        self.historico.append(sessao)
        self.recentes.push(jogo)

        print('Sessao registrada com sucesso.')
        sessao.exibir()
        return True

    def registrar_sessao_manual(self):
        jogo = self.buscar_jogo_por_id()
        if jogo is None:
            return

        registrou = self.registrar_sessao(jogo)
        if registrou:
            self.salvar_historico()
            self.salvar_recentes()

    def mostrar_historico(self):
        if len(self.historico) == 0:
            print('Historico vazio.')
            return

        print('---- HISTORICO DE SESSOES ----')
        for sessao in self.historico:
            sessao.exibir()

    def jogos_jogados(self):
        jogos = []
        for id_jogo in self.tempos_por_jogo:
            jogo = self.jogos_por_id.get(id_jogo)
            if jogo is not None:
                jogos.append(jogo)
        return jogos

    def somar_tempo_por_campo(self, nome_campo):
        dados = {}

        for id_jogo, tempo in self.tempos_por_jogo.items():
            jogo = self.jogos_por_id.get(id_jogo)
            if jogo is None:
                continue

            chave = getattr(jogo, nome_campo)
            if chave == '':
                chave = 'Desconhecido'

            dados[chave] = dados.get(chave, 0.0) + tempo

        return dados

    def maior_item(self, dados):
        maior_chave = None
        maior_valor = 0.0

        for chave, valor in dados.items():
            if maior_chave is None or valor > maior_valor:
                maior_chave = chave
                maior_valor = valor

        return maior_chave, maior_valor

    def status_por_tempo(self, tempo_total):
        if tempo_total < 2:
            return 'iniciado'
        if tempo_total < 10:
            return 'em andamento'
        if tempo_total < 20:
            return 'muito jogado'
        return 'concluído simbolicamente'

    def recomendar_jogos(self, mostrar=True):
        backlog_ids = self.ids_no_backlog()
        genero_favorito, _ = self.maior_item(
            self.somar_tempo_por_campo('genero')
        )
        console_favorito, _ = self.maior_item(
            self.somar_tempo_por_campo('console')
        )
        publisher_favorita, _ = self.maior_item(
            self.somar_tempo_por_campo('publisher')
        )

        recomendacoes = []

        for jogo in self.catalogo:
            if jogo.id in backlog_ids:
                continue

            if self.tempos_por_jogo.get(jogo.id, 0.0) >= 10:
                continue

            pontos = 0.0

            if genero_favorito is not None and jogo.genero == genero_favorito:
                pontos += 3

            if console_favorito is not None and jogo.console == console_favorito:
                pontos += 2

            if (publisher_favorita is not None and
                    jogo.publisher == publisher_favorita):
                pontos += 1

            if jogo.critic_score >= 8:
                pontos += 2

            if jogo.total_sales >= 1:
                pontos += 1

            pontos += jogo.critic_score
            pontos += jogo.total_sales / 5

            if len(self.historico) == 0:
                if jogo.critic_score < 8 and jogo.total_sales < 5:
                    continue
            elif pontos < 8:
                continue

            recomendacoes.append([pontos, jogo])

        recomendacoes.sort(key=lambda item: item[0], reverse=True)
        jogos_recomendados = []

        for item in recomendacoes:
            jogos_recomendados.append(item[1])

        if mostrar:
            print('---- RECOMENDACOES ----')
            print('Criterios usados:')

            if genero_favorito is not None:
                print(f'- Genero mais jogado: {genero_favorito}')
            else:
                print('- Sem genero favorito ainda')

            if console_favorito is not None:
                print(f'- Console mais jogado: {console_favorito}')
            else:
                print('- Sem console favorito ainda')

            if publisher_favorita is not None:
                print(f'- Publisher recorrente: {publisher_favorita}')
            else:
                print('- Sem publisher recorrente ainda')

            print('- Prioridade para nota da critica alta')
            print('- Prioridade para vendas totais altas')
            print('- Evita jogos ja muito jogados e jogos do backlog')
            self.mostrar_resultados(jogos_recomendados[:10], limite=10)

        return jogos_recomendados

    def ranking_jogos_mais_jogados(self):
        ranking = []

        for id_jogo, tempo in self.tempos_por_jogo.items():
            jogo = self.jogos_por_id.get(id_jogo)
            if jogo is not None:
                ranking.append([tempo, jogo])

        ranking.sort(key=lambda item: item[0], reverse=True)

        print('---- JOGOS MAIS JOGADOS ----')
        if len(ranking) == 0:
            print('Nenhum jogo registrado.')
            return ranking

        for posicao, item in enumerate(ranking[:10], start=1):
            tempo = item[0]
            jogo = item[1]
            print(f'{posicao}. {jogo.titulo} - {tempo:.2f} horas')

        return ranking

    def ranking_generos_mais_jogados(self):
        dados = self.somar_tempo_por_campo('genero')
        ranking = sorted(dados.items(), key=lambda item: item[1],
                         reverse=True)

        print('---- GENEROS MAIS JOGADOS ----')
        if len(ranking) == 0:
            print('Nenhum genero registrado.')
            return ranking

        for posicao, item in enumerate(ranking[:10], start=1):
            print(f'{posicao}. {item[0]} - {item[1]:.2f} horas')

        return ranking

    def ranking_consoles_mais_jogados(self):
        dados = self.somar_tempo_por_campo('console')
        ranking = sorted(dados.items(), key=lambda item: item[1],
                         reverse=True)

        print('---- CONSOLES MAIS JOGADOS ----')
        if len(ranking) == 0:
            print('Nenhum console registrado.')
            return ranking

        for posicao, item in enumerate(ranking[:10], start=1):
            print(f'{posicao}. {item[0]} - {item[1]:.2f} horas')

        return ranking

    def ranking_top_notas_historico(self):
        jogos = self.jogos_jogados()
        jogos = sorted(jogos, key=lambda jogo: jogo.critic_score,
                       reverse=True)

        print('---- TOP NOTAS NO HISTORICO ----')
        if len(jogos) == 0:
            print('Nenhum jogo registrado.')
            return jogos

        for posicao, jogo in enumerate(jogos[:10], start=1):
            print(f'{posicao}. {jogo.titulo} - Nota {jogo.critic_score}')

        return jogos

    def mostrar_rankings(self):
        self.ranking_jogos_mais_jogados()
        print()
        self.ranking_generos_mais_jogados()
        print()
        self.ranking_consoles_mais_jogados()
        print()
        self.ranking_top_notas_historico()

    def gerar_ranking_pessoal(self):
        self.mostrar_rankings()

    def contar_status(self):
        contagem = {
            'iniciado': 0,
            'em andamento': 0,
            'muito jogado': 0,
            'concluído simbolicamente': 0
        }

        for tempo in self.tempos_por_jogo.values():
            status = self.status_por_tempo(tempo)
            contagem[status] = contagem.get(status, 0) + 1

        return contagem

    def dashboard(self):
        total_jogado = 0.0
        for tempo in self.tempos_por_jogo.values():
            total_jogado += tempo

        jogos_jogados = self.jogos_jogados()
        ranking_jogos = []

        for id_jogo, tempo in self.tempos_por_jogo.items():
            jogo = self.jogos_por_id.get(id_jogo)
            if jogo is not None:
                ranking_jogos.append([tempo, jogo])

        ranking_jogos.sort(key=lambda item: item[0], reverse=True)

        if len(ranking_jogos) > 0:
            jogo_mais_jogado = ranking_jogos[0][1].titulo
        else:
            jogo_mais_jogado = 'Nenhum'

        genero_favorito, _ = self.maior_item(
            self.somar_tempo_por_campo('genero')
        )
        console_favorito, _ = self.maior_item(
            self.somar_tempo_por_campo('console')
        )

        if genero_favorito is None:
            genero_favorito = 'Nenhum'
        if console_favorito is None:
            console_favorito = 'Nenhum'

        soma_notas = 0.0
        quantidade_notas = 0
        for jogo in jogos_jogados:
            if jogo.critic_score > 0:
                soma_notas += jogo.critic_score
                quantidade_notas += 1

        if quantidade_notas > 0:
            nota_media = soma_notas / quantidade_notas
        else:
            nota_media = 0.0

        contagem_status = self.contar_status()
        recomendacoes = self.recomendar_jogos(mostrar=False)

        if len(self.historico) > 0:
            media_sessao = total_jogado / len(self.historico)
        else:
            media_sessao = 0.0

        jogo_popular = 'Nenhum'
        jogo_melhor_nota = 'Nenhum'

        if len(jogos_jogados) > 0:
            jogo_popular_obj = max(jogos_jogados,
                                   key=lambda jogo: jogo.total_sales)
            jogo_nota_obj = max(jogos_jogados,
                                key=lambda jogo: jogo.critic_score)
            jogo_popular = jogo_popular_obj.titulo
            jogo_melhor_nota = jogo_nota_obj.titulo

        print('======== DASHBOARD STEAMPY ========')
        print(f'Total de jogos no catalogo: {len(self.catalogo)}')
        print(f'Total de jogos no backlog: {self.backlog.tamanho()}')
        print(f'Total de jogos recentes: {self.recentes.tamanho()}')
        print(f'Total de sessoes jogadas: {len(self.historico)}')
        print(f'Tempo total jogado: {total_jogado:.2f} horas')
        print(f'Jogo mais jogado: {jogo_mais_jogado}')
        print(f'Genero favorito: {genero_favorito}')
        print(f'Console favorito: {console_favorito}')
        print(f'Nota media dos jogos jogados: {nota_media:.2f}')
        print(f'Total de jogos iniciados: {contagem_status["iniciado"]}')
        print('Total de jogos em andamento: '
              f'{contagem_status["em andamento"]}')
        print('Total de jogos muito jogados: '
              f'{contagem_status["muito jogado"]}')
        print('Total de jogos concluidos simbolicamente: '
              f'{contagem_status["concluído simbolicamente"]}')
        print(f'Total de recomendacoes disponiveis: {len(recomendacoes)}')
        print(f'Media de horas por sessao: {media_sessao:.2f}')
        print(f'Jogo mais popular ja jogado: {jogo_popular}')
        print(f'Jogo com melhor nota ja jogado: {jogo_melhor_nota}')
        print('===================================')

    def exibir_dashboard(self):
        self.dashboard()

    def salvar_dados(self):
        self.salvar_backlog()
        self.salvar_historico()
        self.salvar_recentes()

    def menu(self):
        while True:
            print()
            print('========== STEAMPY ==========')
            print('1. Carregar catalogo')
            print('2. Listar jogos')
            print('3. Buscar jogo por nome')
            print('4. Filtrar por genero')
            print('5. Filtrar por console')
            print('6. Filtrar por publisher')
            print('7. Filtrar por ano')
            print('8. Filtrar por nota minima')
            print('9. Filtrar por vendas minimas')
            print('10. Ordenar catalogo')
            print('11. Adicionar jogo ao backlog')
            print('12. Ver backlog')
            print('13. Jogar proximo do backlog')
            print('14. Ver jogos recentes')
            print('15. Retomar ultimo jogo')
            print('16. Registrar sessao manualmente')
            print('17. Ver historico de sessoes')
            print('18. Ver recomendacoes')
            print('19. Ver rankings')
            print('20. Ver dashboard')
            print('21. Salvar dados')
            print('0. Sair')
            print('=============================')

            try:
                opcao = input('Escolha uma opcao: ').strip()
            except EOFError:
                self.salvar_dados()
                print('Encerrando o SteamPy.')
                break

            if opcao == '1':
                self.carregar_jogos('dataset.csv')
            elif opcao == '2':
                self.listar_jogos()
            elif opcao == '3':
                self.buscar_por_nome()
            elif opcao == '4':
                self.filtrar_por_genero()
            elif opcao == '5':
                self.filtrar_por_console()
            elif opcao == '6':
                self.filtrar_por_publisher()
            elif opcao == '7':
                self.filtrar_por_ano()
            elif opcao == '8':
                self.filtrar_por_nota_minima()
            elif opcao == '9':
                self.filtrar_por_vendas_minimas()
            elif opcao == '10':
                self.ordenar_catalogo()
            elif opcao == '11':
                self.adicionar_ao_backlog()
            elif opcao == '12':
                self.mostrar_backlog()
            elif opcao == '13':
                self.jogar_proximo_backlog()
            elif opcao == '14':
                self.mostrar_recentes()
            elif opcao == '15':
                self.retomar_ultimo_jogo()
            elif opcao == '16':
                self.registrar_sessao_manual()
            elif opcao == '17':
                self.mostrar_historico()
            elif opcao == '18':
                self.recomendar_jogos()
            elif opcao == '19':
                self.mostrar_rankings()
            elif opcao == '20':
                self.dashboard()
            elif opcao == '21':
                self.salvar_dados()
            elif opcao == '0':
                self.salvar_dados()
                print('SteamPy encerrado. Dados salvos.')
                break
            else:
                print('Opcao invalida. Tente novamente.')
