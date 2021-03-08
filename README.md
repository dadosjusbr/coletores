[![Build Status](https://travis-ci.org/dadosjusbr/coletores.svg?branch=master)](https://travis-ci.org/dadosjusbr/coletores) [![codecov](https://codecov.io/gh/dadosjusbr/coletores/branch/master/graph/badge.svg)](https://codecov.io/gh/dadosjusbr/coletores) [![Go Report Card](https://goreportcard.com/badge/github.com/dadosjusbr/coletores)](https://goreportcard.com/report/github.com/dadosjusbr/coletores)

# Coletores

Coletores de dados sobre remunerações do sistema de justiça brasileiro

## Tutorial

Quer contribuir com a libertação de dados do sistema de justiça do seu estado? Temos um [tutorial](collectors/TUTORIAL.md) para ajudar nessa tarefa.

## Contribuição

Na nomenclatura do DadosJusBR, um coletor (crawler) de remunerações é responsável por duas tarefas: baixar os dados do site oficial do órgão e convertê-los para o formato padronizado de resultado de coleta [Crawling Result](https://github.com/dadosjusbr/storage/blob/master/agency.go#L27). Para facilitar o processo de contruibuição, por favor ler nossas [regras e código de conduta](https://github.com/dadosjusbr/coletores/blob/master/CONTRIBUTING.md). 

## Status

### Coletados e disponibilizados no [site](https://dadosjusbr.org)

- [MPF](https://github.com/dadosjusbr/coletores/tree/master/mpf)
- [MPPB](https://github.com/dadosjusbr/coletores/tree/master/mppb)
- [MPPR](https://github.com/dadosjusbr/coletores/tree/master/mppr)
- [MPM](https://github.com/dadosjusbr/coletores/tree/master/mpm)
- [MPRJ](https://github.com/dadosjusbr/coletores/tree/master/mprj)
- [MPRS](https://github.com/dadosjusbr/coletores/tree/master/mprs)
- [MPSP](https://github.com/dadosjusbr/coletores/tree/master/mpsp)
- [TJPB](https://github.com/dadosjusbr/coletores/tree/master/tjpb)
- [TRT13](https://github.com/dadosjusbr/coletores/tree/master/trt13)
- [TREPB](https://github.com/dadosjusbr/coletores/tree/master/trepb)

### Em progresso ou ainda não são coletados frequentemente

| Nome do Coletor | Coleta | Tradução  |
|:--------------- |:-------------:|:----------------:|
| [MPBA](https://github.com/dadosjusbr/coletores/tree/master/mpba)           | X             |         X        |
| [MPPE](https://github.com/dadosjusbr/coletores/tree/master/mppe)           | X             |         X        |
| [MPBA](https://github.com/dadosjusbr/coletores/tree/master/mpba)           | X             |         X        |
| [TJBA](https://github.com/dadosjusbr/coletores/tree/master/tjba)           |               |         X        |

## Transparência do Sistema de Justiça na Mídia

* 08/03/2021 - [Índice de acesso à justiça (publicado pelo CNJ)](https://www.cnj.jus.br/wp-content/uploads/2021/02/Relatorio_Indice-de-Acesso-a-Justica_LIODS_22-2-2021.pdf)
* 07/09/2020 - [Os privilégios da toga](https://piaui.folha.uol.com.br/os-privilegios-da-toga/)
* 24/08/2020 -[Tribunal de Justiça do Ceará lidera ranking da transparência no País, aponta estudo](https://www.focus.jor.br/tribunal-de-justica-do-ceara-lidera-ranking-da-transparencia-no-pais-aponta-estudo/)
* 23/08/2020 - [Levantamento mostra que tribunais de justiça descumprem leis de transparência](https://congressoemfoco.uol.com.br/opiniao/colunas/levantamento-mostra-que-tribunais-de-justica-descumprem-leis-de-transparencia/)

## Agradecimentos

Esse projeto é fruto da colaboração de muitas pessoas . Entre elas, destacamos (em ordem alfabética):

- [Ana Paula Gomes](https://github.com/anapaulagomes)
- [Aurélio Buarque](https://github.com/ABuarque)
- [Bruno Morassutti](https://github.com/jedibruno)
- [Vinicius Agostini](https://github.com/viniagostini)
- [Tony Messias](https://github.com/tonysm)
