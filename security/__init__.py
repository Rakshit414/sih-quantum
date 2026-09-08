"""
Q-Sentinel: Security, Threat Modeling & Detection Package
"""
from security.signature import (
    SignatureToken,
    QuantumDigitalSignature,
    QDSKeyManager,
    TransmittedQDS,
    distribute_signature_via_teleportation,
)
from security.freshness import FreshnessRegistry
from security.attacks import (
    AttackScenario,
    ThreatOrchestrator,
    apply_quantum_channel_noise,
    simulate_forgery_attack,
    simulate_impersonation_attack,
    simulate_replay_attack,
)
from security.detector import (
    ThreatCategory,
    ThreatAssessment,
    QStatDetector,
)
from security.trojan import (
    StoredQubitState,
    TrojanProbeSignal,
    TrojanDetectionResult,
    QuantumMemoryBuffer,
    TrojanHorseDetector,
)
from security.blind import (
    DetectorTelemetry,
    BlindingDetectionResult,
    DetectorBlindingWatcher,
)
from security.chsh import (
    CHSHMeasurementSetting,
    CHSHVerificationResult,
    CHSHBellWatcher,
)
from security.finite import (
    FiniteKeyParameters,
    FiniteSecurityResult,
    FiniteSizeSecurityAnalyzer,
)
from security.mdi import (
    MDIEvent,
    MDIAnalysisResult,
    MDIQuantumRelay,
    MDIRelayWatcher,
)
from security.wdm import (
    WDMChannelConfig,
    WDMAnalysisResult,
    RamanScatteringModel,
    WDMRamanWatcher,
)

__all__ = [
    "SignatureToken",
    "QuantumDigitalSignature",
    "QDSKeyManager",
    "TransmittedQDS",
    "distribute_signature_via_teleportation",
    "FreshnessRegistry",
    "AttackScenario",
    "ThreatOrchestrator",
    "apply_quantum_channel_noise",
    "simulate_forgery_attack",
    "simulate_impersonation_attack",
    "simulate_replay_attack",
    "ThreatCategory",
    "ThreatAssessment",
    "QStatDetector",
    "StoredQubitState",
    "TrojanProbeSignal",
    "TrojanDetectionResult",
    "QuantumMemoryBuffer",
    "TrojanHorseDetector",
    "DetectorTelemetry",
    "BlindingDetectionResult",
    "DetectorBlindingWatcher",
    "CHSHMeasurementSetting",
    "CHSHVerificationResult",
    "CHSHBellWatcher",
    "FiniteKeyParameters",
    "FiniteSecurityResult",
    "FiniteSizeSecurityAnalyzer",
    "MDIEvent",
    "MDIAnalysisResult",
    "MDIQuantumRelay",
    "MDIRelayWatcher",
    "WDMChannelConfig",
    "WDMAnalysisResult",
    "RamanScatteringModel",
    "WDMRamanWatcher",
]

