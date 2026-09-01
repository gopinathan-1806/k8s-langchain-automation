from .analyzer import KubernetesAnalyzer
from .config import validate_config


HEALTHY_STATUSES = {
    "Running",
    "Succeeded",
}


def print_header():

    print("\n" + "=" * 75)

    print(
        "             Kubernetes AI Troubleshooting Assistant"
    )

    print("=" * 75)


def print_pods(pods):

    print("\nKubernetes Pods")
    print("-" * 75)

    for index, pod in enumerate(
        pods,
        start=1,
    ):

        status = pod["status"]

        marker = (
            "✓"
            if status in HEALTHY_STATUSES
            else "⚠"
        )

        print(
            f"{index:2}. {marker} "
            f"{pod['name']} "
            f"[{status}]"
        )


def main():

    validate_config()

    print_header()

    namespace = input(
        "\nEnter Kubernetes namespace [monitoring]: "
    ).strip()

    if not namespace:

        namespace = "monitoring"

    print(
        f"\nConnecting to IKS namespace: "
        f"{namespace}"
    )

    try:

        analyzer = KubernetesAnalyzer()

        pods = analyzer.kubernetes.get_pods(
            namespace=namespace
        )

    except Exception as exc:

        print(
            f"\n❌ Unable to connect to Kubernetes:\n"
            f"{exc}"
        )

        return

    if not pods:

        print(
            f"\nNo pods found in namespace "
            f"'{namespace}'."
        )

        return

    print_pods(pods)

    problematic_pods = [
        pod
        for pod in pods
        if pod["status"]
        not in HEALTHY_STATUSES
    ]

    if not problematic_pods:

        print("\n✓ No unhealthy pods detected.")

        return

    print(
        f"\n⚠ Detected "
        f"{len(problematic_pods)} "
        f"pod(s) requiring investigation."
    )

    print("\nProblematic Pods")

    for index, pod in enumerate(
        problematic_pods,
        start=1,
    ):

        print(
            f"{index}. "
            f"{pod['name']} "
            f"[{pod['status']}]"
        )

    selection = input(
        "\nSelect pod number to investigate: "
    ).strip()

    try:

        index = int(selection) - 1

        if index < 0 or index >= len(problematic_pods):

            raise ValueError

    except ValueError:

        print("\n❌ Invalid selection.")

        return

    selected = problematic_pods[index]

    pod_name = selected["name"]

    print("\n" + "=" * 75)

    print("                    INCIDENT SELECTED")

    print("=" * 75)

    print(f"\nPod      : {pod_name}")
    print(f"Namespace: {namespace}")
    print(f"Status   : {selected['status']}")
    print(f"Phase    : {selected['phase']}")

    print("\nCollecting live Kubernetes evidence...")

    try:

        result = analyzer.analyze_pod(
            namespace=namespace,
            pod_name=pod_name,
        )

    except Exception as exc:

        print(
            f"\n❌ Analysis failed:\n{exc}"
        )

        return

    print("\n" + "=" * 75)

    print("                    AI ROOT CAUSE ANALYSIS")

    print("=" * 75)

    print("\nIncident")
    print("-" * 75)

    print(result.incident)

    print("\nObserved Facts")
    print("-" * 75)

    for fact in result.observed_facts:

        print(f"• {fact}")

    print("\nRoot Cause")
    print("-" * 75)

    print(result.root_cause)

    print("\nWhy This Is Happening")
    print("-" * 75)

    print(result.why_this_is_happening)

    print("\nEvidence")
    print("-" * 75)

    for evidence in result.evidence:

        print(f"✓ {evidence}")

    print("\nConfidence")
    print("-" * 75)

    print(result.confidence)

    print("\nRecommended Investigation")
    print("-" * 75)

    for recommendation in (
        result.recommended_investigation
    ):

        print(f"{recommendation}")

    print("\nSafe kubectl Commands")
    print("-" * 75)

    for command in result.safe_kubectl_commands:

        print(f"$ {command}")

    print("\n" + "=" * 75)

    print(
        "LangSmith trace generated for this "
        "LLM invocation."
    )

    print("=" * 75)


if __name__ == "__main__":
    main()