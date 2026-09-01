from .models import (
    DiagnosticResult,
    PodContext,
)


class DiagnosticEngine:
    """
    Evidence-driven Kubernetes diagnostic engine.

    This layer performs deterministic analysis before
    the evidence is sent to the LLM.

    It does not modify Kubernetes resources.
    """

    def analyze(
        self,
        context: PodContext,
    ) -> DiagnosticResult:

        evidence = []
        checks = []

        # -----------------------------------------------------
        # Collect evidence
        # -----------------------------------------------------

        for container in context.containers:

            if container.reason:

                evidence.append(
                    f"Container '{container.name}' "
                    f"state reason: {container.reason}"
                )

            if container.image:

                evidence.append(
                    f"Container '{container.name}' "
                    f"image: {container.image}"
                )

            if container.restart_count > 0:

                evidence.append(
                    f"Container '{container.name}' "
                    f"restart count: "
                    f"{container.restart_count}"
                )

            if container.exit_code is not None:

                evidence.append(
                    f"Container '{container.name}' "
                    f"exit code: "
                    f"{container.exit_code}"
                )

        # -----------------------------------------------------
        # Analyze Kubernetes events
        # -----------------------------------------------------

        event_messages = []

        for event in context.events:

            if event.reason and event.message:

                message = (
                    f"Kubernetes event "
                    f"{event.reason}: "
                    f"{event.message}"
                )

                evidence.append(message)

                event_messages.append(
                    event.message.lower()
                )

        # -----------------------------------------------------
        # Logs
        # -----------------------------------------------------

        if context.logs:

            evidence.append(
                "Current container logs are available."
            )

        if context.previous_logs:

            evidence.append(
                "Previous container logs are available."
            )

        # -----------------------------------------------------
        # Deterministic root cause detection
        # -----------------------------------------------------

        combined_events = " ".join(
            event_messages
        )

        failure_type = (
            context.pod_status or "Unknown"
        )

        severity = "MEDIUM"

        # =====================================================
        # IMAGE PULL FAILURE
        # =====================================================

        if self._contains_any(
            combined_events,
            [
                "failed to pull image",
                "errimagepull",
                "imagepullbackoff",
                "back-off pulling image",
            ],
        ):

            failure_type = "ImagePullFailure"

            severity = "HIGH"

            # ---------------------------------------------
            # Registry connectivity
            # ---------------------------------------------

            if self._contains_any(
                combined_events,
                [
                    "i/o timeout",
                    "connection timeout",
                    "context deadline exceeded",
                    "dial tcp",
                    "connection refused",
                    "network is unreachable",
                ],
            ):

                failure_type = (
                    "ImagePullRegistryConnectivity"
                )

                evidence.append(
                    "Image pull failure contains "
                    "network connectivity/timeout evidence."
                )

                checks.extend(
                    [
                        "Verify worker-node connectivity "
                        "to the container registry.",
                        "Check outbound HTTPS connectivity "
                        "from the IKS worker nodes.",
                        "Verify firewall/security-group "
                        "rules allow TCP 443.",
                        "Check registry endpoint DNS "
                        "resolution from the worker nodes.",
                        "Verify the registry is reachable "
                        "from the cluster network.",
                    ]
                )

            # ---------------------------------------------
            # Authentication
            # ---------------------------------------------

            elif self._contains_any(
                combined_events,
                [
                    "unauthorized",
                    "authentication required",
                    "pull access denied",
                    "forbidden",
                ],
            ):

                failure_type = (
                    "ImagePullAuthentication"
                )

                evidence.append(
                    "Registry authentication failure "
                    "was detected in Kubernetes events."
                )

                checks.extend(
                    [
                        "Verify registry credentials.",
                        "Check imagePullSecrets.",
                        "Check the ServiceAccount "
                        "used by the pod.",
                        "Verify the registry permissions "
                        "for the requested image.",
                    ]
                )

            # ---------------------------------------------
            # Image/tag does not exist
            # ---------------------------------------------

            elif self._contains_any(
                combined_events,
                [
                    "manifest unknown",
                    "not found",
                    "repository does not exist",
                    "name unknown",
                ],
            ):

                failure_type = (
                    "ImageNotFound"
                )

                evidence.append(
                    "The registry reported that "
                    "the requested image or tag "
                    "could not be found."
                )

                checks.extend(
                    [
                        "Verify the image repository.",
                        "Verify the image tag.",
                        "Verify the image exists "
                        "in the registry.",
                    ]
                )

            else:

                checks.extend(
                    [
                        "Inspect the image-pull error.",
                        "Verify the image repository.",
                        "Verify the image tag.",
                        "Check registry authentication.",
                        "Check registry connectivity.",
                    ]
                )

        # =====================================================
        # CRASH LOOP
        # =====================================================

        elif self._contains_any(
            combined_events,
            [
                "crashloopbackoff",
            ],
        ):

            failure_type = "CrashLoopBackOff"

            severity = "HIGH"

            checks.extend(
                [
                    "Inspect current container logs.",
                    "Inspect previous container logs.",
                    "Check container exit code.",
                    "Check application startup configuration.",
                    "Check referenced ConfigMaps and Secrets.",
                ]
            )

        # =====================================================
        # OOM
        # =====================================================

        elif self._contains_any(
            combined_events,
            [
                "oomkilled",
                "out of memory",
            ],
        ):

            failure_type = "OOMKilled"

            severity = "HIGH"

            checks.extend(
                [
                    "Inspect container memory limits.",
                    "Inspect memory requests.",
                    "Review application memory usage.",
                    "Inspect previous container logs.",
                ]
            )

        # =====================================================
        # SCHEDULING
        # =====================================================

        elif self._contains_any(
            combined_events,
            [
                "failedscheduling",
                "0/0 nodes are available",
                "0/1 nodes are available",
                "insufficient cpu",
                "insufficient memory",
                "untolerated taint",
                "node affinity",
            ],
        ):

            failure_type = (
                "SchedulingFailure"
            )

            severity = "MEDIUM"

            checks.extend(
                [
                    "Inspect pod scheduling events.",
                    "Check node availability.",
                    "Check CPU and memory requests.",
                    "Check node selectors and affinity.",
                    "Check taints and tolerations.",
                ]
            )

        # =====================================================
        # DEFAULT
        # =====================================================

        else:

            checks.extend(
                [
                    "Inspect pod events.",
                    "Inspect container state.",
                    "Inspect current logs.",
                    "Inspect previous logs.",
                ]
            )

        # -----------------------------------------------------
        # Important: add context phase as evidence
        # -----------------------------------------------------

        if context.phase:

            evidence.insert(
                0,
                f"Pod phase: {context.phase}"
            )

        return DiagnosticResult(
            failure_type=failure_type,
            severity=severity,
            evidence=evidence,
            recommended_checks=checks,
        )

    @staticmethod
    def _contains_any(
        text: str,
        patterns: list[str],
    ) -> bool:

        return any(
            pattern in text
            for pattern in patterns
        )