[![Build Status](https://travis-ci.org/dadosjusbr/coletores.svg?branch=master)](https://travis-ci.org/dadosjusbr/coletores) [![codecov](https://codecov.io/gh/dadosjusbr/coletores/branch/master/graph/badge.svg)](https://codecov.io/gh/dadosjusbr/coletores) [![Go Report Card](https://goreportcard.com/badge/github.com/dadosjusbr/coletores)](https://goreportcard.com/report/github.com/dadosjusbr/coletores)

# Coletores

Coletores de dados sobre remunerações do sistema de justiça brasileiro

## Tutorial

Quer contribuir com a libertação de dados do sistema de justiça do seu estado? Temos um [tutorial](collectors/TUTORIAL.md) para ajudar nessa tarefa.

## Contribuição

Na nomenclatura do DadosJusBR, um coletor (crawler) de remunerações é responsável por duas tarefas: baixar os dados do site oficial do órgão e convertê-los para o formato padronizado de resultado de coleta [Crawling Result](https://github.com/dadosjusbr/storage/blob/master/agency.go#L27). Para facilitar o processo de contruibuição, por favor ler nossas [regras e código de conduta](https://github.com/dadosjusbr/coletores/blob/master/CONTRIBUTING.md). 

## Status

| Nome do Coletor | Coleta | Tradução  |
|:--------------- |:-------------:|:----------------:|
| [mppb](https://github.com/dadosjusbr/coletores/tree/master/mppb)             | X             | X                |
| [trt13](https://github.com/dadosjusbr/coletores/tree/master/trt13)           | X             | X                |
| [trepb](https://github.com/dadosjusbr/coletores/tree/master/trepb)           | X             | X                |
| [tjba](https://github.com/dadosjusbr/coletores/tree/master/tjba)           | X             |         X        |
| [tjpb](https://github.com/dadosjusbr/coletores/tree/master/tjpb)           | X             |         X        |
| [mppe](https://github.com/dadosjusbr/coletores/tree/master/mppe)           | X             |         x        |

## Transparência do Sistema de Justiça na Mídia

* 07/09/2020 - [Os privilégios da toga](https://piaui.folha.uol.com.br/os-privilegios-da-toga/)
* 24/08/2020 -[Tribunal de Justiça do Ceará lidera ranking da transparência no País, aponta estudo](https://www.focus.jor.br/tribunal-de-justica-do-ceara-lidera-ranking-da-transparencia-no-pais-aponta-estudo/)
* 23/08/2020 - [Levantamento mostra que tribunais de justiça descumprem leis de transparência](https://congressoemfoco.uol.com.br/opiniao/colunas/levantamento-mostra-que-tribunais-de-justica-descumprem-leis-de-transparencia/)
