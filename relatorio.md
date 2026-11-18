# O que 999 filmes permitem concluir

## 1 · O catálogo e suas lacunas

Cada linha representa um filme. As notas vão de 7,6 a 9,2. Essa concentração limita a generalização para lançamentos de qualquer qualidade e torna a mediana um ponto de partida competitivo para previsão. A classificação etária está ausente em 101 filmes, a nota da crítica em 157 e a receita em 169. Preservamos os filmes e tratamos as ausências conforme a pergunta. O ano de *Apollo 13* aparece como `PG`. O registro entra nas análises que dispensam ano válido.

**Hipótese A — a cobertura de receita varia por época.** A comparação exige dividir a quantidade de ausências pelo total de filmes da década. Nos anos 1950, faltam 25 de 56 receitas (44,6%). Nos anos 2010, faltam 27 de 242 (11,2%). Os seis filmes dos anos 2020 estão sem receita. Preencher esses campos com zero equivaleria a atribuir uma bilheteria conhecida aos títulos.

Nos anos 1950, a mediana de votos foi de 99.182 entre os 31 filmes com receita e de 58.314 entre os 25 sem receita. O mesmo sentido apareceu em todas as dez décadas comparáveis, com razões entre 1,17 e 6,15. Assim, os filmes que sustentam a análise comercial tendem a ter mais avaliações. A direção do possível viés na receita permanece desconhecida.

**Hipótese B — votação e nota.** A correlação de Spearman compara ordenações e admite relações crescentes ou decrescentes sem exigir proporcionalidade. Nos 999 filmes, votos e nota tiveram correlação de +0,212. Ordenando os filmes por votação, as notas medianas nos quatro quartis foram 7,9, 7,9, 7,8 e 8,1. Há uma associação positiva fraca. Ela descreve a amostra e deixa aberta a causa.

## 2a · Um filme para alguém cujo gosto desconhecemos

Adotamos como critério uma avaliação alta apoiada por muitos votos. A regra adapta a fórmula publicada para o Top 250. O peso da nota individual é `votos / (votos + m)`. Combinamos a nota do filme, com esse peso, e a média do catálogo (7,948), com o peso restante. Escolhemos para `m` a mediana dos votos, 138.356. Com essa votação, cada parcela recebe metade do peso. [Referência metodológica do IMDb](https://help.imdb.com/article/imdb/track-movies-tv/faq-for-imdb-votes/G67Y87TFYYP6TWAV)

*The Godfather* recebeu nota 9,2 e 1.620.367 votos. Sua nota reteve 92,1% do peso, chegando a 9,10. *The Dark Knight* teve mais votos, porém partiu de 9,0 e atingiu 8,94. *The Godfather: Part II* ficou em terceiro, com 8,89. A liderança se manteve ao reduzir `m` pela metade ou dobrá-lo. O ranking usa os 999 filmes e oferece uma indicação geral. A satisfação de uma pessoa específica depende de suas preferências.

## 2b · Faturamento e decisão de produção

Em 830 filmes com receita, o número de votos foi a variável numérica com maior associação de Spearman com `Gross` (+0,700). As correlações com duração, ano, nota IMDb e crítica foram +0,178, +0,175, −0,050 e −0,100. Cada comparação usa os pares disponíveis (829 para ano, 749 para crítica). Nos quartis crescentes de votação, as medianas de receita foram 1,8, 8,2, 48,3 e 129,2 milhões nas unidades da base. Votos futuros são desconhecidos ao decidir produzir. Distribuição e alcance podem influenciar as duas medidas.

**Uma característica disponível no roteiro é o gênero.** Consideramos aventura todo filme cujo conjunto de rótulos inclui `Adventure`. A mediana de receita foi de 120,6 milhões nas 170 aventuras e 15,4 milhões nos 660 demais filmes. A mediana das aventuras também foi maior separadamente nas décadas de 1990, 2000 e 2010. Os valores brutos têm moeda e abrangência não confirmadas e não receberam ajuste de inflação.

**Quão frequente foi um grande sucesso?** Calculamos o percentil 75 da receita dentro de cada década e contamos os títulos que atingiram ou superaram o corte. Isso compara filmes com seus contemporâneos. Dos 829 filmes com ano e bilheteria, 97 de 169 aventuras (57,4%) chegaram ao quarto superior, contra 114 de 660 demais filmes (17,3%). A frequência foi maior em oito das dez décadas. As exceções, 1930 e 1940, tinham três aventuras e uma aventura, respectivamente. Nos anos 1950, ambos os grupos tiveram quatro sucessos, mas os denominadores foram seis e 25. Elevando o corte ao percentil 90, as frequências foram 34,3% e 4,4%.

**Implicação para o estúdio.** Os resultados justificam estudar projetos de aventura. A análise é exploratória, os gêneros podem coexistir, e a amostra exclui muitos tipos de lançamento. Para estimar retorno sobre investimento seriam necessários, entre outros dados, orçamento, distribuição e participação do estúdio na receita.

## 2c · O gênero na sinopse

Todos os filmes têm sinopse. O texto típico contém 24 palavras (mediana) e 895 filmes têm vários gêneros. Tratamos o problema como classificação multirrótulo. Com sorteio fixo (semente 42), reservamos 200 filmes para teste. Em 799 filmes, ajustamos TF-IDF com palavras e pares, removendo termos comuns em inglês, e uma regressão logística balanceada por gênero. A referência constante sugere os gêneros presentes em pelo menos metade do treino, o que resultou apenas em drama.

Para crime, palavras como *murder* e *police* tiveram peso positivo elevado. Em guerra, apareceram *soldiers* e *army*. Em romance, *love* e *meets*. Em biografia, *true story*. Essas associações ajudam a interpretar o vocabulário do catálogo. Em *Anatomy of a Murder*, o modelo recuperou crime e mistério, deixando drama de fora. Em *Gone Girl*, recuperou drama e mistério, sugeriu romance e omitiu suspense.

**Decisão interativa sobre a métrica.** A ordem dos rótulos é irrelevante. Escolhemos o Jaccard médio por filme: quantidade de gêneros em comum dividida pela quantidade de gêneros distintos entre previsão e cadastro. Para acertar dois dos três gêneros sem acréscimos indevidos, o filme recebe 2/3. A precisão por filme, nesse mesmo exemplo, seria 100%. Adotamos zero para precisão sem sugestões (oito filmes).

O Jaccard foi de **39,5%** com texto e **36,6%** com a regra constante. A precisão por filme foi de 59,0% contra 78,5%. Agregando as decisões individuais sobre gêneros, a precisão micro foi 58,2%, a cobertura 46,3% e o F1 micro 0,516, ante 78,5%, 31,1% e 0,445 da referência. O conjunto completo foi recuperado em 17 de 200 filmes, ante 21 com a referência. O texto é mais promissor para sugerir temas a um curador do que para catalogar automaticamente todos os gêneros.

## 3 · Estimativa retrospectiva da nota IMDb

Prever uma quantidade numérica é regressão. Os dados do exemplo incluem informações coletadas depois da estreia, portanto adotamos esse momento de uso. Usamos ano e duração em minutos para contexto, nota da crítica como outra medida de recepção, número de votos para participação do público e faturamento para desempenho comercial. Removemos separadores de milhar da receita e aplicamos `log(1+x)` a votos e receita para comprimir as caudas, especialmente no modelo linear. A imputação por mediana com indicadores de ausência foi ajustada no treino de cada rodada. A Ridge também padroniza as entradas. Gênero, elenco e sinopse permanecem candidatos a outros experimentos.

Reservamos 200 filmes com sorteio fixo e usamos validação cruzada de cinco partes nos 799 restantes. Escolhemos **MAE**, pois mede a distância absoluta média em pontos de nota. A mediana do treino serve de referência simples. A regressão Ridge permite examinar coeficientes e capta efeitos lineares. A floresta aleatória permite interações e relações não lineares, com menor transparência e capacidade limitada de extrapolação. Testamos 300 árvores com pelo menos cinco observações por folha.

| Modelo | MAE em validação | MAE no teste | RMSE no teste | R² no teste |
|---|---:|---:|---:|---:|
| Mediana | 0,2169 | 0,2070 | 0,2585 | −0,0176 |
| Ridge | 0,1650 | — | — | — |
| Floresta aleatória | **0,1469** | **0,1535** | **0,1969** | **0,4094** |

A floresta venceu na validação. Avaliamos o vencedor e a referência no teste. O erro absoluto médio caiu aproximadamente 26%. Ao retirar votos, mantendo a floresta e as mesmas partições, o MAE de validação subiu para 0,1975. Esse resultado explica por que mantivemos votos apesar da correlação isolada fraca com nota. A avaliação mede generalização dentro deste catálogo restrito. Um uso antes da estreia exigiria redefinir os campos e validar outro modelo.

## 4 e 5 · Previsão individual e modelo salvo

Para *The Shawshank Redemption*, fornecemos ano 1994, duração de 142 minutos, crítica 80, 2.343.110 votos e receita de 28.341.469. O modelo estimou **8,7361**, ou **8,7** na escala apresentada ao leitor. O MAE resume o desempenho coletivo e não constitui intervalo de confiança individual.

O pickle contém a transformação dos campos, a imputação e a floresta ajustada aos 799 filmes de desenvolvimento. Conservamos esse ajuste para distribuir exatamente o modelo avaliado. A verificação de serialização exigiu igualdade das 200 previsões antes e depois do recarregamento. O exemplo de inferência também foi executado em processo separado.

As [tabelas de evidências](evidencias.md) permitem conferir os denominadores, exemplos e comparações apresentados no relatório.
