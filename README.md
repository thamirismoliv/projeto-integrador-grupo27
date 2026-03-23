# 📊 Projeto Integrador: desenvolvimento low code em ciências de dados

## Tema do Projeto

**Tema:** Análise de desempenho de e-commerce e satisfação do cliente no Brasil

**Contexto:**
O crescimento do e-commerce no Brasil trouxe desafios relacionados à logística, prazos de entrega e experiência do cliente. Com múltiplos fatores influenciando a jornada de compra, torna-se essencial analisar dados para identificar padrões, gargalos e oportunidades de melhoria no processo.


**Objetivo:**
analisar o desempenho das vendas, prazos de entrega e nível de satisfação dos clientes a partir dos dados do Olist. Busca-se identificar fatores que impactam a experiência de compra, gerar insights sobre eficiência logística e qualidade dos produtos, e apoiar a tomada de decisão baseada em dados.

---

## Integrantes do Grupo


* [DIEGO DE SOUZA BRITO](https://github.com/diegosbrito)
* [ELLEN CRISTINA SANTOS DO PRADO](https://github.com/pradoellen-design)
* [GIOVANNA DE OLIVEIRA MANGUEIRA](https://github.com/giovanna27oliveira-lang)
* [JOÃO ANTÔNIO PEREIRA LEMOS MACHADO](https://github.com/joaoaplm-svg)
* [LUCAS SULZBACH RILHO](https://github.com/srJupi)
* [LUIZ GUSTAVO DA SILVA PEREIRA](https://github.com/gugarosp)
* [THAMIRIS MOTA DE OLIVEIRA](https://github.com/thamirismoliv)

---

## Base de Dados

### 🔹 Base escolhida

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### 🔹 Descrição breve da base

Este dataset contém aproximadamente 100 mil pedidos de um e-commerce brasileiro (Olist) realizados entre 2016 e 2018. Ele permite analisar pedidos sob diversas dimensões, como status, pagamentos, frete, localização dos clientes, atributos dos produtos e avaliações. Os dados são anonimizados e organizados em múltiplas tabelas relacionáveis, possibilitando análises completas do processo de compra.

### 🔹 Justificativa da escolha

A base foi escolhida por ser rica, realista e multidimensional, permitindo explorar todo o processo de vendas em e-commerce. Ela é ideal para aplicar técnicas de ETL com Pandas e gerar insights relevantes sobre vendas, logística e satisfação do cliente. Além disso, seu volume e estrutura são adequados para desenvolvimento de dashboards interativos com Streamlit.

---

## Planejamento do Projeto

### 🔹 Cronograma e divisão de tarefas

| Etapa | Descrição                          | Responsável | Prazo    |
|-------|------------------------------------|-------------|----------|
| 1     | Scrum Master & Documentação        | Lucas       | Contínuo |
| 2     | Engenharia de Dados (Extração)     | João        | Semana 1 |
| 3     | Engenharia de Dados (Limpeza)      | Gustavo     | Semana 2 |
| 4     | Analista de Dados (KPIs)           | Thamiris    | Semana 3 |
| 5     | Analista de Dados (Transformação)  | Giovanna    | Semana 4 |
| 6     | Desenvolvedor Streamlit (Layout)   | Diego       | Semana 5 |
| 7     | Desenvolvedor Streamlit (Gráficos) | Ellen       | Semana 6 |
| 8     | Revisão Final & Entrega do Projeto | Todos       | Semana 7 |

---

## Transformações Planejadas

- **Extração de dados**
  - Carregar tabelas principais do dataset Olist
    - orders
    - order_items
    - order_payments
    - order_reviews
    - products
    - customers
    - geolocation


- **Limpeza de dados**
  - Converter colunas de data para formato `datetime`
  - Tratar pedidos com status:
    - canceled
    - unavailable
  - Tratar valores nulos
    - review_score
    - order_delivered_customer_date
    - product_category_name
  - Remover registros duplicados


- **Integração de dados (JOINs)**


- **Criação de novas variáveis**


---

## Visualizações e Métricas

### 🔹 Visualizações planejadas

- **Visão geral (dashboard)**
  - cards de métricas:
    - faturamento total
    - total de pedidos
    - ticket médio
    - nota média de avaliação


- **Análise temporal**
  - gráfico de linha
    - vendas por mês


- **Análise de produtos**
  - gráfico de barras
    - top 10 categorias mais vendidas


- **Pagamentos**
  - gráfico pizza ou donut
    - distribuição dos métodos de pagamento


- **Logística**
  - histograma ou boxplot
    - distribuição do tempo de entrega
  - gráfico de barras
    - prazo médio de entrega por estado


- **Satisfação do cliente**
  - histograma
    - distribuição das avaliações
  - scatter plot
    - atraso na entrega vs avaliação


- **Distribuição geográfica**
  - mapa de calor
    - concentração de pedidos por localização

### 🔹 Métricas principais

- **Métricas de vendas**
  - faturamento total
  - número total de pedidos
  - ticket médio
  - vendas por categoria de produto
  - vendas por região (estado)


- **Métricas logísticas**
  - prazo médio de entrega
  - percentual de entregas atrasadas
  - tempo médio de atraso
  - prazo médio de entrega por estado


- **Métricas de satisfação do cliente**
  - nota média de avaliação
  - distribuição das avaliações (1–5 estrelas)
  - relação entre atraso de entrega e avaliação

---

## Tecnologias

Sugestão de estrutura:

* Linguagem: **Python** <img src="https://raw.githubusercontent.com/bablubambal/All_logo_and_pictures/7c0ac2ceb9f9d24992ec393d11fa7337d2f92466/programming%20languages/python.svg" width="16">
* Bibliotecas: **Pandas, NumPy, Matplotlib**
* Visualização: **Streamlit**
* Versionamento: **Git + GitHub**

---

## Estrutura do Repositório

```
📦 projeto-integrador
 ┣ 📂 data
 ┣ 📂 src
 ┣ 📂 dashboard
 ┗ 📄 README.md
```

---

## Como Utilizar Esse Repositório

*[Descrever o passo a passo de como utilizar esse repositório]*

---

## 📎 Observações

*[Espaço livre para decisões do grupo, alinhamentos ou mudanças futuras]*
