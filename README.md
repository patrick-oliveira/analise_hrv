# Análise de Séries Temporais de Batimentos Cardiacos

### Descrição

Arquivos utilizados para a análise de dados de séries temporais de eletrocardiograma com a finalidade de identificar quantificadores capazes de caracterizar estágios de apneia do sono. Como principais métodos de análise, utilizou-se um algoritmo de segmentação não-paramétrica baseada na estatística de Kolmogorov-Smirnov e o método de Análise de Flutuações Depuradas (DFA), um método tradicional de análise de séries temporais não-estacionárias.

O projeto foi executado no contexto de um edital de iniciação científica da UFABC, com o auxílio financeiro da CNPq.

Trabalhos anteriores e que serviram de base para este trabalho podem ser encontrados na literatura:

[1]: S. Camargo, M. Riedl, C. Anteneodo, N. Wessel, and J. Kurths, Diminished heart beat nonstationarities in congestive heart failure, Frontiers in Physiology 7, 107 (2013).

[1]: S. Camargo, M. Riedl, C. Anteneodo, J. Kurths, T. Penzel, and N. Wessel, Sleep Apnea-Hypopnea Quantification by Cardiovascular Data Analysis, PLoS ONE 9, e107581 (2014).

Obs: O repositório está um tanto bagunçado e espero, num futuro próximo, refazer a análise e reescrever os scripts, ao passo que no intervalo entre a conclusão do projeto e hoje (03/11/2020), aprimorei consideravelmente meus conhecimentos em Python.

### Arquivos

- dfa_functions.py: contém todas as funções relacionadas ao método DFA.
- segmentation_algorithm.py: contém o algoritmo de segmentação.
- Os notebooks estão separados pelo sistema de classificação considerado (4 ou 6 fases) e o que foi feito (ex: aplicação do DFA ou do DFA_L)
