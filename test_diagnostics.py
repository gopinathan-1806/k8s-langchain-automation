from apps.kubernetes_client import KubernetesClient
from apps.diagnostic_engine import DiagnosticEngine


def main():

    namespace = "monitoring"

    kubernetes = KubernetesClient()

    diagnostic_engine = DiagnosticEngine()

    pods = kubernetes.get_pods(
        namespace
    )

    print("\nKubernetes Pods")
    print("=" * 60)

    for pod in pods:

        print(
            f"{pod['name']} "
            f"-> {pod['status']}"
        )

    print("\nLooking for unhealthy pods...")
    print("=" * 60)

    unhealthy = [
        pod
        for pod in pods
        if pod["status"]
        not in {"Running", "Succeeded"}
    ]

    if not unhealthy:

        print(
            "No unhealthy pods found."
        )

        return

    pod = unhealthy[0]

    print(
        f"\nInvestigating:\n"
        f"{pod['name']}\n"
        f"Status: {pod['status']}"
    )

    context = kubernetes.get_pod_context(
        namespace=namespace,
        pod_name=pod["name"],
    )

    diagnostic = diagnostic_engine.analyze(
        context
    )

    print("\nDiagnostic Result")
    print("=" * 60)

    print(
        diagnostic.model_dump_json(
            indent=2
        )
    )


if __name__ == "__main__":
    main()