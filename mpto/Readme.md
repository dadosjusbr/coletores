# Ministério Público do Estado do Tocantins

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos membros ativos do Ministério Público do Estado do Tocantins nos anos 2018, 2019, 2020 e 2021. O site com as informações pode ser acessado [aqui](https://mpto.mp.br/transparencia/webdocs).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de planilhas, no formato ODS, sendo cada uma referente a uma dessas categorias:

- Folha de remuneração: Membros Ativos - As planilhas deste tipo, com exceção das dos colaboradores, seguem o formato seguinte:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Remuneração do Cargo Efetivo (Number)**: Subsídio dos membros do Ministério Público, proventos de membros e servidores do Ministério Público, vencimento básico, gratificação por exercício de atividades perigosas dos secretários de diligências, parcela de readaptação e outras verbas de mesma natureza.
- **Outras Verbas Remuneratórias, Legais ou Judiciais (Number)**: Adicional por tempo de serviço, avanços trienais, FG incorporada, AS incorporada, gratificações incorporadas e outras verbas de mesma natureza.
- **Função de Confiança ou Cargo em Comissão (Number)**: Gratificações de direção, chefe de gabinete, procurador-assessor, promotor-assessor, promotor-corregedor e coordenador de centro de apoio operacional. Função Gratificada (servidor efetivo) ou remuneração de cargo em comissão e outras verbas de mesma natureza.
- **Gratificação Natalina (Number)**: Parcelas da gratificação natalina (13º) pagas no mês corrente.
- **Férias Constitucionais (Number)**: Adicional correspondente a 1/3 (um terço) da remuneração, pago a membros e servidores por ocasião das férias.
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao membro ou servidor que esteja em condição de aposentar-se, mas que optou por continuar em atividade, em conformidade com o Art. 40, § 19, da Constituição Federal.
- **Outras Remunerações Temporárias (Number)**: Valores pagos a título de adicional de insalubridade ou de periculosidade, adicional noturno, serviço extraordinário, substituição de função, gratificação de diretor de promotoria de justiça, gratificação de difícil provimento e gratificação por participação em órgãos colegiados.
- **Verbas Indenizatórias (Number)**: Auxílio-alimentação, auxílio-moradia, auxílio-transporte, auxílio-creche, abono-família, férias não usufruídas e outras verbas de mesma natureza.
- **Total de Rendimentos Brutos (Number)**: Total dos rendimentos brutos pagos no mês.
- **Contribuição Previdenciária (Number)**: Contribuição Previdenciária Oficial (IPERGS ou INSS) e IPERGS-Saúde.
- **Imposto de Renda (Number)**: Imposto de Renda Retido na Fonte.
- **Retenção por Teto Constitucional (Number)**: Valor deduzido da remuneração bruta, quando esta ultrapassa o teto constitucional, de acordo com a Resolução nº 09/2006 do CNMP.
- **Total de Descontos (Number)**: Soma dos descontos referidos nos itens 8, 9 e 10.
- **Rendimento Líquido Total (Number)**: Rendimento líquido após os descontos referidos nos itens anteriores.


- Verbas Indenizatórias e outras remunerações temporárias. Seguem o formato seguinte:

- **Matrícula (String)**: Matrícula do funcionário.
- **Nome (String)**: Nome completo do funcionário.
- **Cargo (String)**: Cargo do funcionário dentro do MP.
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha.
- **Verbas Indenizatórias**: Auxílio-Alimentação, Auxílio-Moradia, Férias Indenizadas, Licença Prêmio Indenizada e outras dessa natureza.
- **Outras Remunerações Temporárias**: Valores pagos a título de cumulações, complementos por entrância e outros dessa natureza.