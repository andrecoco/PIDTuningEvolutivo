# Sintonia de controle PID com AG

Alunos | NUSP
-------|------
André Bermudes Viana | 10684580
Maurício Gabriel Garcia Catellan | 10716592
Rodrigo Augusto Valeretto | 10684792

## Introdução
Esse projeto é relativo à disciplina de Sistemas Evolutivos e Aplicados à Robótica (SSC0713) ministrada no segundo semestre do ano de 2021 pelo Prof. Dr. Eduardo do Valle Simões na Universidade de São Paulo.

O projeto e o código são detalhados no vídeo abaixo.

[![Link para o vídeo](https://img.youtube.com/vi/W_xRHc-kPz0/0.jpg)](https://www.youtube.com/watch?v=W_xRHc-kPz0)

## Explicando o problema
Um controle PID é um sistema de controle que reune as ações proporcional, integral e derivativa em um único sistema. A componente proporcional é responsável por diminuir o erro; a integral, por zerar o erro em regime permanente; e a derivativa atua considerando a taxa da variação do erro.

A ideia do algoritmo é encontrar uma sintonia para um sistema composto por uma lâmpada incandescente, uma ventoinha e um sensor de temperatura. Porém, devido à necessidade de se testar diversas sintonias em pouco tempo, resolvemos utilizar uma simulação, modelando o sistema como um FODPT (First Order plus Dead Time).

O código responsável pela simulação foi baseado no seguinte repositório: https://github.com/Destination2Unknown/PythonPID_Simulator

Para medir a efetividade da sintonia, são considerados os seguintes fatores:
- Erro Médio 
- Variabilidade
- Integral do Erro Absoluto
- Número de Cruzamento do Setpoint
- Percurso da saída do controle
- Número de Reversões da saída do controle
- Erro ao final da simulação
- Consumo de Potência (a saída do controle no exemplo era a potência da lâmpada)

## Explicando a solução
O algoritmo inicializa uma população de indivíduos aleatoriamente. Os genes de cada indivíduo são compostos por um valor de Kp, um de Ki e um de Kd. O fitness de cada um, ou seja, o quão boa é sua sintonia, é calculado. O melhor indivíduo é separado, e todo o resto da população é substituída por novos indivíduos gerados pelo cruzamento do melhor com todos os demais, processo chamado de Elitismo.

Além disso, todos os novos indivíduos sofrem uma mutação em seus genes de acordo com a taxa de mutação.

Após testes, optou-se por utilizar algumas técnicas especiais para melhorar o algoritmo.

### Mutação Variável
A taxa de mutação não permanece a mesma durante toda a execucação do algoritmo. Com isso, obtemos simultaneamente os benefícios de uma taxa de mutação pequena, que é melhorar a convergência da solução, e os de uma taxa mais alta, que aumenta a diversidade, permitindo escapar de mínimos locais. 

### Genocídio
Caso a população passe muitas gerações sem melhoria, todo os indivíduos, com exceção do melhor, são substituídos por indivíduos aleatórios, aumentando a diversidade da população.

### Predação Randômica
Periodicamente, os piores indivíduos de cada geração são substituídos por indivíduos aleatórios, aumentando a diversidade da população.

![Plot_Fitness](https://user-images.githubusercontent.com/16878985/149593476-a51a3021-328f-4cce-b157-0399687452fa.png)


## Instruções de Execução
São requisitos as seguintes bibliotecas de Python:
- Numpy
- Scipy
- Numba
- Matplotlib

Os parâmetros relacionados à evolução podem ser alterados no início do código do arquivo ```main.py```.

A pasta SerialEvo contém os arquivos para evolução utilizando o Arduino, e a pasta Simulacao contém os arquivos que utilizam a simulação.

## Por que Python?
A linguagem Python não é conhecida pelo seu desempenho, algo importante em AG, principalmente se comparada a C/C++. 

Porém, escolhemo-na por conta da simulação da planta seguindo um modelo FODPT, a qual já utiliza algumas funções do Scipy que se aproveitam de código compilado para acelerar o processamento. Além disso, utilizamos multiprocessing e JIT Compilation com o Numba; com o primeiro, conseguimos em nossos testes aumentar em 4x o tamanho da população sem afetar o tempo total, e com o segundo, aumentamos em 2-3x o desempenho total do programa.

