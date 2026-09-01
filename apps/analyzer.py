from .diagnostic_engine import DiagnosticEngine
from .kubernetes_client import KubernetesClient
from .llm import create_llm
from .models import TroubleshootingResponse
from .prompts import KUBERNETES_TROUBLESHOOTING_PROMPT


class KubernetesAnalyzer:

    def __init__(self):

        self.kubernetes = KubernetesClient()

        self.diagnostics = DiagnosticEngine()

        self.llm = create_llm()

        self.structured_llm = (
            self.llm.with_structured_output(
                TroubleshootingResponse
            )
        )

    def analyze_pod(
        self,
        namespace: str,
        pod_name: str,
    ) -> TroubleshootingResponse:

        # -----------------------------------------------------
        # STEP 1
        # Collect live Kubernetes evidence
        # -----------------------------------------------------

        context = (
            self.kubernetes.get_pod_context(
                namespace=namespace,
                pod_name=pod_name,
            )
        )

        # -----------------------------------------------------
        # STEP 2
        # Deterministic diagnostic analysis
        # -----------------------------------------------------

        diagnostic_result = (
            self.diagnostics.analyze(
                context
            )
        )

        # -----------------------------------------------------
        # STEP 3
        # Build LangChain prompt
        # -----------------------------------------------------

        prompt = (
            KUBERNETES_TROUBLESHOOTING_PROMPT.invoke(
                {
                    "pod_name": pod_name,
                    "namespace": namespace,

                    "failure_type": (
                        diagnostic_result.failure_type
                    ),

                    "severity": (
                        diagnostic_result.severity
                    ),

                    "evidence": "\n".join(
                        f"- {item}"
                        for item
                        in diagnostic_result.evidence
                    ),

                    "checks": "\n".join(
                        f"- {item}"
                        for item
                        in diagnostic_result.recommended_checks
                    ),

                    "context": (
                        context.model_dump_json(
                            indent=2
                        )
                    ),
                }
            )
        )

        # -----------------------------------------------------
        # STEP 4
        # LLM reasoning
        # -----------------------------------------------------

        response = (
            self.structured_llm.invoke(
                prompt
            )
        )

        return response