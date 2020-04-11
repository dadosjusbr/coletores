# Status Package

Esse pacote tem o objetivo de padronizar os status de execução dos coletores.

## Status disponíveis

Abaixo segue uma tabela com os status disponíveis:

| Status code | Significado |
--------------|----------
|OK| O processo ocorreu sem erros.|
|InvalidParameters|Deve ser utilizado em caso de parâmetros inválidos, como ano e mês.|
|SystemError|Deve ser usado em casos como falha ao criar o diretório dos arquivos ou na leitura de arquivos.|
|ConnectionError|Deve ser usado em problemas de conexão, como timeout ou serviço fora do ar.|
|DataUnavailable|A informação solicitada não foi encontrada, provavelmente o órgão não o disponibiliou ainda.|
|InvalidFile| Deve ser usado para cenários onde o arquivo não é o esperado ou em caso de falhas na extração de dados.|
|Unexpected|Deve ser usando quando um erro inesperado ocorrer.|
______________

## Exemplo de uso
```
import (
	"fmt"
    "https://github.com/dadosjusbr/coletores/status"
)

func myFunc() *StatusError {
  // code
  return status.NewStatusError(status.DataUnavailable, err.Error())
}

func main() {
  err := myFunc()
  status.ExitFromError(err)
}
```