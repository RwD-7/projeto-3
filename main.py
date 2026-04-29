from Steam import SteamPy


def main():
    sistema = SteamPy()
    sistema.carregar_jogos('dataset.csv')
    sistema.carregar_backlog()
    sistema.carregar_historico()
    sistema.carregar_recentes()
    sistema.menu()


if __name__ == '__main__':
    main()
