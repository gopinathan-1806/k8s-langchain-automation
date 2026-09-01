from pydantic import BaseModel, Field


class ContainerInfo(BaseModel):
    name: str
    image: str | None = None
    state: str | None = None
    reason: str | None = None
    exit_code: int | None = None
    signal: int | None = None
    restart_count: int = 0
    ready: bool = False


class EventInfo(BaseModel):
    type: str | None = None
    reason: str | None = None
    message: str | None = None
    timestamp: str | None = None


class PodContext(BaseModel):
    name: str
    namespace: str
    phase: str | None = None
    pod_status: str | None = None
    node_name: str | None = None

    containers: list[ContainerInfo] = Field(
        default_factory=list
    )

    events: list[EventInfo] = Field(
        default_factory=list
    )

    logs: str = ""
    previous_logs: str = ""


class DiagnosticResult(BaseModel):
    failure_type: str
    severity: str

    evidence: list[str] = Field(
        default_factory=list
    )

    recommended_checks: list[str] = Field(
        default_factory=list
    )


class TroubleshootingResponse(BaseModel):
    incident: str

    observed_facts: list[str] = Field(
        default_factory=list
    )

    root_cause: str

    why_this_is_happening: str

    evidence: list[str] = Field(
        default_factory=list
    )

    confidence: str

    recommended_investigation: list[str] = Field(
        default_factory=list
    )

    safe_kubectl_commands: list[str] = Field(
        default_factory=list
    )