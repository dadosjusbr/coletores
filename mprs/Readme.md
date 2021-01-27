# Ministério Público do Estado do Rio Grande do Sul

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Estado do Rio Grande do Sul nos anos 2018, 2019 e 2020. O site com as informações pode ser acessado [aqui](https://transparencia.mprs.mp.br/contracheque/).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de planilhas, no formato CSV, sendo cada uma referente a uma dessas categorias:

- Tipo I - Folha de remuneração: Membros Ativos, Membros Inativos, Servidores Ativos, Servidores Inativos, Pensionistas, Colaboradores. As planilhas deste tipo, com exceção das dos colaboradores, seguem o formato seguinte:

- **Nome (String)**: Nome completo do funcionário.
- **Matrícula (String)**: Matrícula do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Remuneração do Cargo Efetivo (Number)**: Subsídio dos membros do Ministério Público, proventos de membros e servidores do Ministério Público, vencimento básico, gratificação por exercício de atividades perigosas dos secretários de diligências, parcela de readaptação e outras verbas de mesma natureza.
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: Adicional por tempo de serviço, avanços trienais, FG incorporada, AS incorporada, gratificações incorporadas e outras verbas de mesma natureza.
- **Função de Confiança ou Cargo em Comissão (Number)**: Gratificações de direção, chefe de gabinete, procurador-assessor, promotor-assessor, promotor-corregedor e coordenador de centro de apoio operacional. Função Gratificada (servidor efetivo) ou remuneração de cargo em comissão e outras verbas de mesma natureza.
- **Gratificação Natalina (Number)**: Parcelas da gratificação natalina (13º) pagas no mês corrente.
- **Férias (1/3 constitucional) (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago a membros e servidores por ocasião das férias.
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao membro ou servidor que esteja em condição de aposentar-se, mas que optou por continuar em atividade, em conformidade com o Art. 40, § 19, da Constituição Federal.
- **Outras remunerações retroativas/Temporárias (Number)**: Valores pagos a título de adicional de insalubridade ou de periculosidade, adicional noturno, serviço extraordinário, substituição de função, gratificação de diretor de promotoria de justiça, gratificação de difícil provimento e gratificação por participação em órgãos colegiados.
- **Indenizações (Number)**: Auxílio-alimentação, auxílio-moradia, auxílio-transporte, auxílio-creche, abono-família, férias não usufruídas e outras verbas de mesma natureza.
- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (IPERGS ou INSS) e IPERGS-Saúde.
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração bruta, quando esta ultrapassa o teto constitucional, de acordo com a Resolução nº 09/2006 do CNMP.
- **Total de Descontos (Number)**: Soma dos descontos referidos nos itens 8, 9 e 10.
- **Total Líquido (Number)**: Rendimento obtido após o abatimento dos descontos referidos no item 11. O valor líquido efetivamente recebido pelo membro ou servidor pode ser inferior ao ora divulgado, porque não são considerados os descontos de caráter pessoal.

As planilhas dos colaboradores (estagiários), por sua vez, seguem o formato seguinte:

- **NOME (String)**: Nome completo do funcionário.
- **BOLSA-AUXÍLIO - HORAS (Number)**: Horas cumpridas na função.
- **BOLSA-AUXÍLIO - VALOR (Number)**: Valor bruto da bolsa-auxílio.
- **BENEFÍCIO - QTD. (Number)**:
- **BENEFÍCIO - VALOR (Number)**: Valor bruto dos benefícios recebidos.
- **INDENIZAÇÃO DE RECESSO (Number)**: Quando os dias a que o Estagiário tem direito lhe são pagos.
- **DESCONTOS (Number)**:  Impostos e taxas a serem abatidas da remuneração
- **REMUNERAÇÃO LÍQUIDA (Number)**: Valor líquido, retirados os descontos.

- Tipo II - Verbas Referentes a exercícios anteriores. Apesar de não coletarmos essas planilhas, elas seguem o formato seguinte:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Nr. Processo (String)**: Número do processo com a devida caracterização de seu órgão de origem.
- **Objeto do Processo (String)**: Denomnação da verba objeto do processo ou justificativa do pagamento.
- **Origem do Processo (String)**: Classificação do processo de concessão da verba como de natureza judicial ou administrativa.
- **Valor Bruto (Number)**: Valor bruto recebido no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (IPERGS ou INSS) e IPERGS-Saúde.
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Total de Descontos (Number)**: Soma dos descontos efetuados.
- **Valor Líquido (Number)**: Valor líquido recebido.

- Tipo III - Verbas Indenizatórias e outras remunerações temporárias. Seguem o formato seguinte:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Verbas Indenizatórias**: Auxílio-alimentação, Auxílio-transporte, Auxílio-moradia, Ajuda de Custo e outras dessa natureza, exceto diárias, que serão divulgadas no Portal Transparência, discriminada de forma individualizada.
- **Outras Remunerações Temporárias**: Valores pagos a título de Adicional de Insalubridade ou de Periculosidade, Adicional Noturno, Serviço Extraordinário, Substituição de Função, Cumulações.

## Dificuldades para libertação dos dados

Observa-se, no site, um formato diferente na apresentação dos dados dos colaboradores. Tanto a interface de busca quanto a apresentação da tabela diferem do padrão utilizado nas demais planilhas, bem como a URL de acesso ao download, que normalmente é assim "https://transparencia.mprs.mp.br/contracheque/download/M/2020/01/NORMAL/", mas nessa área é assim "https://transparencia.mprs.mp.br/contracheque/estagiarios/?ano=2020&mes=1&procurar=+Procurar+#".

Não foi possível identificar o significado do campo "QTD.", quarta coluna presente na planilha de colaboradores. Disponível [aqui](https://transparencia.mprs.mp.br/contracheque/estagiarios/)