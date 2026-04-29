

# Projeto 3 — SteamPy

Projeto desenvolvido para a disciplina de **Programação de Computadores**.

O **SteamPy** é um sistema em Python que simula uma plataforma simples de organização, consumo e análise de jogos digitais. O programa carrega um catálogo de jogos a partir de um arquivo CSV, permite buscar e filtrar jogos, montar um backlog pessoal, registrar sessões jogadas, visualizar jogos recentes, gerar recomendações, rankings e um dashboard analítico.

## Objetivo

O objetivo do projeto é aplicar estruturas de dados e conceitos fundamentais de programação em Python, incluindo:

- variáveis
- condicionais
- laços de repetição
- funções
- manipulação de arquivos
- listas
- dicionários
- classes
- fila
- pilha
- ordenação
- filtros
- análise simples de dados

## Funcionalidades

O sistema permite:

- carregar um catálogo de jogos a partir do arquivo `dataset.csv`;
- listar jogos do catálogo;
- buscar jogos por nome;
- filtrar jogos por gênero;
- filtrar jogos por console;
- filtrar jogos por publisher;
- filtrar jogos por ano de lançamento;
- filtrar jogos por nota mínima;
- filtrar jogos por vendas mínimas;
- ordenar o catálogo por diferentes critérios;
- adicionar jogos ao backlog;
- jogar o próximo jogo do backlog;
- visualizar o backlog;
- registrar sessões de jogo;
- visualizar histórico de sessões;
- visualizar jogos recentes;
- retomar o último jogo jogado;
- gerar recomendações com base no perfil do usuário;
- gerar rankings pessoais;
- exibir um dashboard com estatísticas gerais;
- salvar e carregar dados entre execuções.

## Estruturas utilizadas

### Lista

Usada para armazenar:

- catálogo de jogos;
- histórico de sessões;
- resultados de buscas e filtros;
- rankings;
- recomendações.

### Dicionário

Usado para:

- indexar jogos por ID;
- armazenar tempos acumulados por jogo;
- gerar estatísticas por gênero, console e publisher.

### Fila

A fila é usada no backlog.

O primeiro jogo adicionado ao backlog será o primeiro a ser jogado.

Arquivo responsável:

```text
filabacklog.py
