# =================================================================================
# PUCPR - Escola Politécnica
# Computação Quântica - Simulação de Ruído em Circuitos Quânticos
# Grupo 1: Kelvin C. Ribas, Marcos P. Ruppel, Rafael A. Souza, Rafaelle Lemichka
# =================================================================================

from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
from dotenv import load_dotenv
from qiskit_ibm_runtime import (
    QiskitRuntimeService,
    SamplerV2 as Sampler
)
import matplotlib.pyplot as plt
import os

load_dotenv()

TOKEN = os.getenv("IBM_QUANTUM_TOKEN")
INSTANCE = os.getenv("IBM_QUANTUM_INSTANCE")

QiskitRuntimeService.save_account(
    token=TOKEN, # Use the 44-character API_KEY you created and saved from the IBM Quantum Platform Home dashboard
    instance=INSTANCE, # Optional
    overwrite=True
)

# =====================================================
# PASTA DOS GRÁFICOS
# =====================================================

os.makedirs("graficos", exist_ok=True)

# =====================================================
# CIRCUITOS
# =====================================================

def bell_phi_plus():
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.cx(0,1)
    qc.measure([0,1],[0,1])
    return qc

def bell_phi_minus():
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.z(0)
    qc.cx(0,1)
    qc.measure([0,1],[0,1])
    return qc

def bell_psi_plus():
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.cx(0,1)
    qc.x(1)
    qc.measure([0,1],[0,1])
    return qc

def bell_psi_minus():
    qc = QuantumCircuit(2,2)
    qc.h(0)
    qc.cx(0,1)
    qc.x(1)
    qc.z(0)
    qc.measure([0,1],[0,1])
    return qc

def ghz():
    qc = QuantumCircuit(3,3)
    qc.h(0)
    qc.cx(0,1)
    qc.cx(1,2)
    qc.measure([0,1,2],[0,1,2])
    return qc

def codificacao_densa():
    qc = QuantumCircuit(2,2)

    # Criação Bell
    qc.h(0)
    qc.cx(0,1)

    # Mensagem "10"
    qc.z(0)

    # Decodificação
    qc.cx(0,1)
    qc.h(0)

    qc.measure([0,1],[0,1])

    return qc

# =====================================================
# LISTA DE CIRCUITOS
# =====================================================

circuitos = [
    (bell_phi_plus(), "Bell_Phi_Plus"),
    (bell_phi_minus(), "Bell_Phi_Minus"),
    (bell_psi_plus(), "Bell_Psi_Plus"),
    (bell_psi_minus(), "Bell_Psi_Minus"),
    (ghz(), "GHZ"),
    (codificacao_densa(), "Dense_Coding")
]

# =====================================================
# SIMULADORES
# =====================================================

ideal_sim = AerSimulator()

# =====================================================
# CONECTAR IBM QUANTUM
# =====================================================

print("Conectando a IBM Quantum Cloud...")

service = QiskitRuntimeService()

# Escolhe o backend mais estável
backend = service.least_busy(operational=True, min_num_qubits=100)

print(f"Backend selecionado: {backend.name}")

sampler = Sampler(backend)

# =====================================================
# EXECUTAR HARDWARE REAL
# =====================================================

shots = 1024

print("\nExecutando em hardware real...")

qcs = [qc for qc, nome in circuitos]

# transpile para hardware
qcs_real = transpile(qcs, backend)

job = sampler.run(qcs_real, shots=shots)

print(f"Job enviado.")
print(f"Job ID: {job.job_id()}")

real_result = job.result()

# Guardar resultados reais
resultados_reais = {}

for i, (qc, nome) in enumerate(circuitos):

    counts_real = real_result[i].data.c.get_counts()
    resultados_reais[nome] = counts_real

    print(f"\nResultado REAL {nome}")
    print(counts_real)

# =====================================================
# TESTAR DIFERENTES RUÍDOS (ISOLADOS POR TIPO)
# =====================================================

valores_p = [0.01, 0.1, 0.3, 0.5]
tipos_ruido = ['X', 'Y', 'Z']

for tipo in tipos_ruido:
    for p in valores_p:

        print("\n====================================")
        print(f"Executando ruído {tipo} com p = {p}")
        print("====================================")

        # -------------------------------------------------
        # MODELO DE RUÍDO ISOLADO
        # -------------------------------------------------

        error_1q = pauli_error([
            (tipo, p),
            ('I', 1-p)
        ])

        error_2q = error_1q.tensor(error_1q)

        noise_model = NoiseModel()

        noise_model.add_all_qubit_quantum_error(
            error_1q,
            ['h', 'x', 'z']
        )

        noise_model.add_all_qubit_quantum_error(
            error_2q,
            ['cx']
        )

        noisy_sim = AerSimulator(noise_model=noise_model)

        # =================================================
        # EXECUTAR CIRCUITOS
        # =================================================

        for qc, nome in circuitos:

            # ---------------------------------------------
            # IDEAL
            # ---------------------------------------------

            tqc_ideal = transpile(qc, ideal_sim)

            result_ideal = ideal_sim.run(
                tqc_ideal,
                shots=shots
            ).result()

            counts_ideal = result_ideal.get_counts()

            # ---------------------------------------------
            # COM RUÍDO
            # ---------------------------------------------

            tqc_noisy = transpile(qc, noisy_sim)

            result_noisy = noisy_sim.run(
                tqc_noisy,
                shots=shots
            ).result()

            counts_noisy = result_noisy.get_counts()

            # ---------------------------------------------
            # REAL
            # ---------------------------------------------

            counts_real = resultados_reais[nome]

            # =================================================
            # PRINT RESULTADOS
            # =================================================

            print(f"\nCircuito: {nome}")
            print("Ideal:", counts_ideal)
            print(f"Ruído ({tipo}):", counts_noisy)
            print("Hardware Real:", counts_real)

            # =================================================
            # HISTOGRAMA
            # =================================================

            fig = plot_histogram(
                [
                    counts_ideal,
                    counts_noisy,
                    counts_real
                ],
                legend=[
                    'Ideal',
                    f'Ruído {tipo} (p={p})',
                    'Hardware Real'
                ],
                title=f'{nome} | Ruído: {tipo} | Probabilidade: {p}',
                figsize=(12,7)
            )

            # Nome do arquivo agora especifica o tipo de ruído e a probabilidade
            nome_arquivo = f"graficos/{nome}_Ruido{tipo}_p_{p}.png"

            fig.savefig(nome_arquivo)
            plt.close(fig)

            print(f"Gráfico salvo: {nome_arquivo}")

print("\nTODAS AS EXECUÇÕES FINALIZADAS.")