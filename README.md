# Sintonia de controle PID com AG

Alunos | NUSP
-------|------
André Bermudes Viana | 10684580
Maurício Gabriel Garcia Catellan | 10716592
Rodrigo Augusto Valeretto | 10684792

## Introdução
Esse projeto é relativo à disciplina de Sistemas Evolutivos e Aplicados à Robótica (SSC0713) ministrada no segundo semestre do ano de 2021 pelo Prof. Dr. Eduardo do Valle Simões na Universidade de São Paulo.

## Explicando o problema
Um controle PID é um sistema de controle que reune as ações proporcional, integral e derivativa. A componente proporcional é responsável por diminuir o erro, a integral por zerar o erro em regime permanente, e a derivativa atua considerando a taxa da variação do erro.

A ideia do algoritmo era encontrar uma sintonia para um sistema composto por uma lâmpada incandescente, uma ventoinha e um sensor de temperatura. Porém devido a necessidade de se testar diversas sintonias em pouco tempo, resolvemos então utilizar uma simulação, modelando o sistema como um FODPT (First Order plus Dead Time).

O código responsável pela simulação foi baseado nesse repositório: https://github.com/Destination2Unknown/PythonPID_Simulator

Para medir a efetividade da sintonia são considerados os seguintes fatores:
- Erro Médio 
- Variabilidade
- Integral do Erro Absoluto
- Número de Cruzamento do Setpoint
- Percurso da saída do controle
- Número de Reversões da saída do controle
- Erro ao final da simulação
- Consumo de Potência (a saída do controle no exemplo era a potência da lâmpada)

## Explicando a solução
O algoritmo inicializa uma população de indivíduos (com genes compostos por um valor de Kp, Ki e Kd) aleatoriamente. O fitness de cada indivíduo, ou seja, o quão bom é sua sintonia, é calculado. O melhor indivíduo é separado, e todo o resto da população é substituída por novos indivíduos gerados pelo cruzamento do melhor com todos os demais, processo chamado Elitismo.

Além disso, todos os novos indivíduos sofrem uma mutação em seus genes de acordo com a taxa de mutação.

Após testes, algumas técnicas especiais foram utilizadas para melhorar o algoritmo.

### Mutação Variável
A taxa de mutação não permanece a mesma durante toda a execucação do algoritmo, mas varia, com isso obtemos simultaneamente os benefícios de uma taxa de mutação pequena, que é melhorar a convergência da solução, e os de uma taxa mais alta, que aumenta a diversidade, permitindo escapar de mínimos locais. 

### Genocídio
Caso a população passe muitas gerações sem melhoria, todo os indivíduos, com exceção do melhor, são substituídos por indivíduos aleatórios, aumentando a diversidade da população.

### Predação Randômica
Periodicamente, os piores indivíduos de cada geração são substituídos por indivíduos aleatórios, aumentando a diversidade da população.

## Instruções de Execução
São requisitos as seguintes bibliotecas de Python:
- Numpy
- Scipy
- Numba
- Matplotlib

Os parâmetros relacionados à evolução podem ser alterados no início do código do arquivo ```main.py```.

A pasta SerialEvo contém os arquivos para evolução utilizando o Arduino, e a pasta Simulacao contém os arquivos utilizando a simulação.
