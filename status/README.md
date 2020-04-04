# Status Package

Esse pacote tem o objetivo de padronizar os status de execução dos coletores.

## Status disponíveis

| Status code | Significado |
--------------|----------
|OK| O processo ocorreu sem erros.|
|ServiceUnavailable|O website que fornece a informação está fora do ar.|
|RequestTimeout|A requisição dos dados resultou em um timeout.|
|DataUnavailable|A informação solicitada não foi encontrada, provavelmente o órgão não o disponibiliou ainda.|
|ParsingError| Algum erro não específico ocorreu durante o processo de parsing.|
______________

## Exemplo de uso
```
import (
	"fmt"
    "https://github.com/dadosjusbr/coletores"
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