# Contributing to Q-Sentinel

Thank you for your interest in contributing to **Q-Sentinel: Quantum-Inspired Cyber Threat Detection Framework** (Smart India Hackathon SIH-26141 · National Quantum Mission Track).

---

## 🏛️ Core Engineering Invariants

Before submitting any code, verify your implementation adheres to our foundational project constraints:

1. **Strictly Zero AI/ML / Neural Network Dependencies**:
   * Per Problem Statement SIH26141, all threat detection, security scoring, and anomaly bounds must be **100% mathematically deterministic** (derived from quantum projective measurements, exact binomial hypothesis testing, Page's CUSUM, or Wald's SPRT).
   * No PyTorch, TensorFlow, Scikit-Learn, or black-box heuristic models may be imported.

2. **AST Import Boundary Isolation**:
   * The decoupled microservices (`Alice`, `Eve`, `Bob`) must maintain strict process isolation.
   * `transport/bob_node.py` and `transport/alice_node.py` must never import `transport/eve_channel.py` or simulate attacks out-of-band.

3. **100% Test Pass Invariant**:
   * All pull requests must pass the complete 130-test regression suite:
     ```bash
     python run_tests.py
     ```

---

## 🛠️ Development Setup

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/Rakshit414/sih-quantum.git
   cd sih-quantum
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate       # Windows: .venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```

3. **Run Test Suite**:
   ```bash
   python run_tests.py
   ```

4. **Run Release Audit**:
   ```bash
   python run_audit.py
   ```

---

## 📝 Pull Request Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit with conventional commit messages:
   * `feat(...)`: New feature or detector
   * `fix(...)`: Bug fix or test correction
   * `docs(...)`: Documentation or paper update
   * `test(...)`: Additional test cases
3. Ensure no trailing whitespace or lint issues.
4. Open a Pull Request against `main`.

---

## 💬 Community & Support

* **Project Lead**: Rakshit Jain
* **Team**: Team QUANT
* **Mission**: Smart India Hackathon 2026 (SIH-26141) — National Quantum Mission Track
