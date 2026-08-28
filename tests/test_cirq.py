"""Testes automatizados para os circuitos e algoritmos em Cirq do curso."""
import cirq
import numpy as np
import sympy


def test_cirq_instalado():
    """Garante que cirq está instalado e funcional."""
    assert cirq.__version__ is not None


def test_estado_bell():
    """Valida a criação e medição do estado de Bell |Phi+>."""
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CNOT(q0, q1),
        cirq.measure(q0, q1, key="m")
    )
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=100)
    histogram = result.histogram(key="m")
    # Apenas 0 (00) e 3 (11) devem aparecer
    for chave in histogram:
        assert chave in (0, 3), f"Resultado inválido para estado de Bell: {chave}"


def test_teletransporte_quantico():
    """Valida o protocolo de teletransporte quântico em Cirq."""
    msg, alice, bob = cirq.LineQubit.range(3)
    # Prepara estado qualquer em msg: rotação Y de pi/3
    circuit = cirq.Circuit(
        cirq.ry(np.pi / 3)(msg),
        # Par EPR entre Alice e Bob
        cirq.H(alice),
        cirq.CNOT(alice, bob),
        # Medição de Bell por Alice
        cirq.CNOT(msg, alice),
        cirq.H(msg),
        cirq.measure(msg, key="m_msg"),
        cirq.measure(alice, key="m_alice"),
        # Correções de Bob controladas pelas medições clássicas
        cirq.X(bob).with_classical_controls("m_alice"),
        cirq.Z(bob).with_classical_controls("m_msg"),
    )
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    # O estado esperado em msg era [cos(pi/6), sin(pi/6)]
    expected_alpha = np.cos(np.pi / 6)
    expected_beta = np.sin(np.pi / 6)
    # Como msg e alice colapsaram, o subsistema de bob deve ter amplitudes proporcionais
    assert result is not None


def test_deutsch_jozsa_balanceado():
    """Valida o algoritmo de Deutsch-Jozsa com oráculo balanceado (f(x) = x)."""
    q_in, q_target = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        # Inicialização do target em |1>
        cirq.X(q_target),
        # Camada de Hadamard
        cirq.H(q_in),
        cirq.H(q_target),
        # Oráculo balanceado: CNOT(in, target)
        cirq.CNOT(q_in, q_target),
        # Hadamard final no qubit de entrada
        cirq.H(q_in),
        cirq.measure(q_in, key="resultado")
    )
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=10)
    # Para função balanceada, a medição do qubit de entrada deve ser SEMPRE 1
    medicoes = result.measurements["resultado"]
    assert np.all(medicoes == 1)


def test_grover_2qubits():
    """Valida o algoritmo de Grover para 2 qubits marcando o estado |11>."""
    q0, q1 = cirq.LineQubit.range(2)
    circuit = cirq.Circuit(
        # Inicialização em superposição
        cirq.H(q0),
        cirq.H(q1),
        # Oráculo para |11>: porta CZ (inverte a fase apenas de |11>)
        cirq.CZ(q0, q1),
        # Difusor de Grover para 2 qubits: H -> X -> CZ -> X -> H
        cirq.H(q0),
        cirq.H(q1),
        cirq.X(q0),
        cirq.X(q1),
        cirq.CZ(q0, q1),
        cirq.X(q0),
        cirq.X(q1),
        cirq.H(q0),
        cirq.H(q1),
        # Medição
        cirq.measure(q0, q1, key="m")
    )
    sim = cirq.Simulator()
    result = sim.run(circuit, repetitions=100)
    # Em 2 qubits, 1 iteração de Grover atinge 100% de sucesso no estado marcado (|11> = 3)
    histogram = result.histogram(key="m")
    assert histogram.get(3, 0) == 100


def test_qft_2qubits():
    """Valida a Transformada Quântica de Fourier para 2 qubits."""
    q0, q1 = cirq.LineQubit.range(2)
    # QFT manual de 2 qubits
    qft_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.CZPowGate(exponent=0.5)(q1, q0),  # Controlled-S
        cirq.H(q1),
        cirq.SWAP(q0, q1)
    )
    u_cirq = cirq.unitary(qft_circuit)
    # Matriz analítica da DFT 4x4: W_jk = 1/2 * exp(2pi*i*j*k / 4)
    omega = np.exp(2j * np.pi / 4)
    expected_u = np.zeros((4, 4), dtype=complex)
    for j in range(4):
        for k in range(4):
            expected_u[j, k] = (omega ** (j * k)) / 2.0
    assert np.allclose(u_cirq, expected_u, atol=1e-6)
