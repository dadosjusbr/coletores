# Ministério Público de Pernambuco - Crawler

Este crawler tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público de Pernambuco. O site com as informações pode ser acessado [aqui](https://transparencia.mppe.mp.br/contracheque).

O crawler está estruturado como uma CLI. Você passa dois argumentos (mês e ano) e serão baixadas oito planilhas no formato XLSX, 

## Como usar

- É preciso ter o compilador de Go instalado em sua máquina. Mais informações [aqui](https://golang.org/dl/).
- Rode o comando abaixo, com mês e ano que você quer ter acesso as informações

```sh
cd crawler/mppe
go build
./mppe.go --mes=${MES} --ano=${ANO}
```

## Dicionário de Dados
