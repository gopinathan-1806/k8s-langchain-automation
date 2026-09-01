from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

from .models import (
    ContainerInfo,
    EventInfo,
    PodContext,
)


class KubernetesClient:
    """
    Read-only Kubernetes client.

    This class only retrieves information from Kubernetes.
    It does not modify cluster resources.
    """

    def __init__(self):

        try:
            config.load_kube_config()
        except Exception as exc:
            raise RuntimeError(
                "Unable to load Kubernetes configuration. "
                "Make sure kubectl is configured correctly."
            ) from exc

        self.core_v1 = client.CoreV1Api()

    # ---------------------------------------------------------
    # POD LIST
    # ---------------------------------------------------------

    def get_pods(
        self,
        namespace: str,
    ) -> list[dict]:

        try:

            pods = self.core_v1.list_namespaced_pod(
                namespace=namespace
            )

        except ApiException as exc:

            raise RuntimeError(
                f"Unable to retrieve pods from "
                f"namespace '{namespace}': {exc}"
            ) from exc

        results = []

        for pod in pods.items:

            results.append(
                {
                    "name": pod.metadata.name,
                    "namespace": pod.metadata.namespace,
                    "phase": (
                        pod.status.phase
                        if pod.status
                        else None
                    ),
                    "node_name": (
                        pod.spec.node_name
                        if pod.spec
                        else None
                    ),
                    "status": self._get_pod_status(pod),
                }
            )

        return results

    # ---------------------------------------------------------
    # POD DIAGNOSTICS
    # ---------------------------------------------------------

    def get_pod_context(
        self,
        namespace: str,
        pod_name: str,
    ) -> PodContext:

        try:

            pod = self.core_v1.read_namespaced_pod(
                name=pod_name,
                namespace=namespace,
            )

        except ApiException as exc:

            raise RuntimeError(
                f"Unable to retrieve pod "
                f"'{pod_name}' in namespace "
                f"'{namespace}': {exc}"
            ) from exc

        containers = (
            self._extract_container_information(pod)
        )

        events = self._get_pod_events(
            namespace,
            pod_name,
        )

        logs = self._get_pod_logs(
            namespace,
            pod,
            previous=False,
        )

        previous_logs = self._get_pod_logs(
            namespace,
            pod,
            previous=True,
        )

        return PodContext(
            name=pod.metadata.name,
            namespace=namespace,
            phase=(
                pod.status.phase
                if pod.status
                else None
            ),
            pod_status=self._get_pod_status(pod),
            node_name=(
                pod.spec.node_name
                if pod.spec
                else None
            ),
            containers=containers,
            events=events,
            logs=logs,
            previous_logs=previous_logs,
        )

    # ---------------------------------------------------------
    # CONTAINER INFORMATION
    # ---------------------------------------------------------

    def _extract_container_information(
        self,
        pod,
    ) -> list[ContainerInfo]:

        containers = []

        specs = (
            pod.spec.containers
            if pod.spec and pod.spec.containers
            else []
        )

        statuses = {}

        if pod.status and pod.status.container_statuses:

            statuses = {
                status.name: status
                for status in pod.status.container_statuses
            }

        for container in specs:

            status = statuses.get(container.name)

            state = None
            reason = None
            exit_code = None
            signal = None
            restart_count = 0
            ready = False

            if status:

                restart_count = (
                    status.restart_count or 0
                )

                ready = bool(status.ready)

                if status.state:

                    if status.state.waiting:

                        state = "Waiting"

                        reason = (
                            status.state.waiting.reason
                        )

                    elif status.state.running:

                        state = "Running"

                    elif status.state.terminated:

                        state = "Terminated"

                        reason = (
                            status.state.terminated.reason
                        )

                        exit_code = (
                            status.state.terminated.exit_code
                        )

                        signal = (
                            status.state.terminated.signal
                        )

            containers.append(
                ContainerInfo(
                    name=container.name,
                    image=container.image,
                    state=state,
                    reason=reason,
                    exit_code=exit_code,
                    signal=signal,
                    restart_count=restart_count,
                    ready=ready,
                )
            )

        return containers

    # ---------------------------------------------------------
    # EVENTS
    # ---------------------------------------------------------

    def _get_pod_events(
        self,
        namespace: str,
        pod_name: str,
    ) -> list[EventInfo]:

        try:

            events = (
                self.core_v1.list_namespaced_event(
                    namespace=namespace
                )
            )

        except ApiException:

            return []

        results = []

        for event in events.items:

            if not event.involved_object:
                continue

            if event.involved_object.name != pod_name:
                continue

            timestamp = None

            if event.last_timestamp:

                timestamp = (
                    event.last_timestamp.isoformat()
                )

            elif event.event_time:

                timestamp = (
                    event.event_time.isoformat()
                )

            results.append(
                EventInfo(
                    type=event.type,
                    reason=event.reason,
                    message=event.message,
                    timestamp=timestamp,
                )
            )

        return results

    # ---------------------------------------------------------
    # LOGS
    # ---------------------------------------------------------

    def _get_pod_logs(
        self,
        namespace: str,
        pod,
        previous: bool,
    ) -> str:

        if not pod.spec:
            return ""

        if not pod.spec.containers:
            return ""

        sections = []

        for container in pod.spec.containers:

            try:

                logs = (
                    self.core_v1
                    .read_namespaced_pod_log(
                        name=pod.metadata.name,
                        namespace=namespace,
                        container=container.name,
                        tail_lines=100,
                        previous=previous,
                    )
                )

                if logs:

                    label = (
                        "Previous"
                        if previous
                        else "Current"
                    )

                    sections.append(
                        f"--- {label} logs: "
                        f"{container.name} ---\n"
                        f"{logs}"
                    )

            except ApiException:

                continue

        return "\n\n".join(sections)

    # ---------------------------------------------------------
    # POD STATUS
    # ---------------------------------------------------------

    @staticmethod
    def _get_pod_status(pod) -> str:

        if not pod.status:
            return "Unknown"

        if pod.status.phase == "Pending":
            return "Pending"

        if pod.status.phase == "Succeeded":
            return "Succeeded"

        if pod.status.phase == "Failed":
            return "Failed"

        if pod.status.phase == "Running":

            if pod.status.container_statuses:

                for status in (
                    pod.status.container_statuses
                ):

                    if status.state:

                        if status.state.waiting:

                            reason = (
                                status.state.waiting.reason
                            )

                            if reason:
                                return reason

                        if status.state.terminated:

                            reason = (
                                status.state.terminated.reason
                            )

                            if reason:
                                return reason

            return "Running"

        return pod.status.phase