# Status Package

Esse pacote tem o objetivo de padronizar os status de execução dos coletores.

## Status disponíveis

Os códigos de status disponíveis seguem uma ordem semântica:
+ Em caso de sucesso tem-se valor 0;
+ Em caso de erro durante o processo de setup, out seja, antes do crawling, os erros pertecem iniciam em 100 e podem ir até 199;
+ Em caso de erro durante o crawling os erros iniciam em 200;
+ Em caso de erro durante do parsing os erros iniciam em 300;
+ Erros não previstos iniciam em 400;

Abaixo segue uma tabela com os status disponíveis:

| Status code | Significado |
--------------|----------
|OK| O processo ocorreu sem erros.|
|MonthAndYearNotProvided|Deve ser usado quando o mês e ano para serem consultados não forem informados|
|InvalidMonth|Deve ser usado quando o mês informado for inválido|
|InvalidYear|Deve ser usado quando o ano informado for inválido|
|CouldNotCreateDirectory|Deve ser usado quando ocorrer um erro criando o diretório de arquivos do coletor|
|ServiceUnavailable|O website que fornece a informação está fora do ar.|
|RequestTimeout|A requisição dos dados resultou em um timeout.|
|DataUnavailable|A informação solicitada não foi encontrada, provavelmente o órgão não o disponibiliou ainda.|
|CouldNotOpenFile| Deve ser usado quando não for possível abrir o arquivo durante o parsing.|
|CouldNotExtractData|Deve ser usado quando ocorrer erro extraingo algum dado do arquivo durante o parsing.|
|Unexpected|Deve ser usando quando um erro inesperado ocorrer.|
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