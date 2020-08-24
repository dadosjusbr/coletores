[![Build Status](https://travis-ci.org/dadosjusbr/coletores.svg?branch=master)](https://travis-ci.org/dadosjusbr/coletores) [![codecov](https://codecov.io/gh/dadosjusbr/coletores/branch/master/graph/badge.svg)](https://codecov.io/gh/dadosjusbr/coletores) [![Go Report Card](https://goreportcard.com/badge/github.com/dadosjusbr/coletores)](https://goreportcard.com/report/github.com/dadosjusbr/coletores)

# Coletores

Coletores de dados sobre remunerações do sistema de justiça brasileiro

## Tutorial

Quer contribuir com a libertação de dados do sistema de justiça do seu estado? Temos um [tutorial](TUTORIAL.md) para ajudar nessa tarefa.

## Status

Na nomenclatura do DadosJusBR, um coletor (crawler) de remunerações é responsável por duas tarefas: baixar os dados do site oficial do órgão e convertê-los para o formato padronizado de resultado de coleta (crawling result). Para facilitar o processo de revisão, aconselhamos que separem a automação do download dos arquivos e da tradução em dois PRs, sendo o segundo aberto depois do primeiro ter sido aprovado. O órgão só fará parte do processo de libertação contínua quando ambas as etapas forem concluídas.


| Nome do Coletor | Coleta | Tradução  |
|:--------------- |:-------------:|:----------------:|
| [mppb](https://github.com/dadosjusbr/coletores/tree/master/mppb)             | X             | X                |
| [trt13](https://github.com/dadosjusbr/coletores/tree/master/trt13)           | X             | X                |
| [trepb](https://github.com/dadosjusbr/coletores/tree/master/trepb)           | X             | X                |
| [tjpb](https://github.com/dadosjusbr/coletores/tree/master/tjpb)           | X             |         X        |
| [mppe](https://github.com/dadosjusbr/coletores/tree/master/mppe)           | X             |         x        |

## Transparência do Sistema de Justiça na Mídia

* 23/08/2020 - [Levantamento mostra que tribunais de justiça descumprem leis de transparência](https://congressoemfoco.uol.com.br/opiniao/colunas/levantamento-mostra-que-tribunais-de-justica-descumprem-leis-de-transparencia/)
