# Simulação de Ruído em Circuitos Quânticos

Este projeto foi desenvolvido para a disciplina de **Computação Quântica** da **PUCPR (Escola Politécnica)**. O objetivo principal é analisar como o ruído quântico afeta diferentes circuitos e comparar os resultados entre simulações ideais, simulações com ruído de Pauli e execuções em hardware real da IBM Quantum.

## 👥 Grupo 1
* Kelvin C. Ribas
* Marcos P. Ruppel
* Rafael A. Souza
* Rafaelle Lemichka

**Professor:** Rodrigo Pasti  
**Data:** Maio de 2026

## 🎯 Objetivos
* Compreender o conceito de decoerência e ruído em computação quântica.
* Implementar e analisar ruídos de Pauli ($X, Y, Z$).
* Comparar a distribuição de probabilidades de circuitos ideais versus ruidosos.
* Avaliar a fidelidade de resultados obtidos em computadores quânticos reais (IBM Quantum).

## 🛠️ Tecnologias e Bibliotecas
* **Python 3.x**
* **Qiskit**: Framework para programação quântica.
* **Qiskit Aer**: Simulador de alto desempenho com suporte a modelos de ruído.
* **Qiskit IBM Runtime**: Interface para execução em hardware real.
* **Matplotlib**: Geração de histogramas e visualização de dados.
* **python-dotenv**: Gerenciamento de credenciais.

## ↔️ Circuitos Implementados
O projeto avalia o impacto do ruído nos seguintes circuitos clássicos:
1.  **Estados de Bell**: As quatro variações ($\Phi^+, \Phi^-, \Psi^+, \Psi^-$) para testar emaranhamento máximo.
2.  **Estado GHZ**: Emaranhamento estendido para 3 qubits.
3.  **Codificação Densa**: Protocolo de comunicação quântica para transmissão de 2 bits clássicos.

## 📊 Metodologia de Teste
O script `main.py` realiza as seguintes etapas:
1.  **Execução Ideal**: Simulação sem ruído para estabelecer o benchmark.
2.  **Hardware Real**: Envio dos circuitos para o backend da IBM Quantum menos ocupado.
3.  **Simulação de Ruído Isolada**: Testes iterativos variando a probabilidade de erro ($p = 0.01, 0.1, 0.3, 0.5$) para cada tipo de canal de Pauli ($X, Y$ e $Z$) individualmente.
4.  **Comparação**: Geração automática de histogramas na pasta `/graficos` unificando os três cenários para análise estatística.

## ⚙️ Como Executar

### 1. Pré-requisitos
Instale as dependências necessárias:

```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime matplotlib python-dotenv
```

### 2. Configuração da API IBM
Crie um arquivo .env na raiz do projeto com suas credenciais da IBM Quantum:
```python
IBM_QUANTUM_TOKEN=seu_token_aqui
IBM_QUANTUM_INSTANCE=CRN_aqui
````

### 3. Execução
Execute o script principal para iniciar as simulações e coletas:
```bash
python main.py
```
## 🎓 Resultados e Conclusões
- Ruído X (Bit-Flip): Altera diretamente os estados lógicos, sendo facilmente perceptível em qualquer circuito.
- Ruído Z (Phase-Flip): É "invisível" em medições simples na base computacional (como na Codificação Densa), mas degrada severamente estados que dependem de interferência de fase, como o GHZ.
- Hardware Real: Os processadores da IBM apresentam uma fidelidade superior a simulações com $p \geq 0.1$, comportando-se de forma similar a um modelo de ruído com $p \approx 0.02$, embora apresentem erros sistemáticos de leitura (readout errors).

---
Projeto acadêmico desenvolvido para fins de estudo sobre a era NISQ (Noisy Intermediate-Scale Quantum)
