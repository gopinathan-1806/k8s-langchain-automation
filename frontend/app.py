import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

import streamlit as st

from apps.analyzer import KubernetesAnalyzer
from apps.config import validate_config


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="K8s AI Doctor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "pods": [],
    "analysis_result": None,
    "namespace": "monitoring",
    "selected_pod": None,
    "connection_error": None,
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   APPLICATION
   ============================================================ */

.stApp {
    background-color: #080c14;
}

.block-container {
    max-width: 1500px;

    /*
       Important:
       Adds enough space below Streamlit's top toolbar
       so that the application header is not clipped.
    */
    padding-top: 3.5rem;
    padding-bottom: 3rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background-color: #060a11;

    border-right: 1px solid #1d2635;
}

section[data-testid="stSidebar"] .block-container {

    padding-top: 1.8rem;
}


/* ============================================================
   HEADER
   ============================================================ */

.header-title {

    font-size: 2rem;

    font-weight: 800;

    color: #f8fafc;

    letter-spacing: -0.04em;

    line-height: 1.25;

    padding-top: 0.25rem;
}


.header-subtitle {

    color: #718096;

    font-size: 0.78rem;

    margin-top: 0.4rem;
}


.header-status {

    text-align: right;

    font-size: 0.68rem;

    font-weight: 800;

    letter-spacing: 0.08em;

    padding-top: 0.45rem;
}


.header-online {

    color: #4ade80;
}


.header-offline {

    color: #f87171;
}


/* ============================================================
   SECTION LABEL
   ============================================================ */

.section-label {

    color: #64748b;

    font-size: 0.66rem;

    font-weight: 800;

    letter-spacing: 0.14em;

    margin-top: 1.6rem;

    margin-bottom: 0.7rem;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

div[data-testid="stMetric"] {

    background-color: #0d141f;

    border: 1px solid #202c3d;

    border-radius: 12px;

    padding: 1rem;
}


div[data-testid="stMetricLabel"] {

    color: #718096;
}


div[data-testid="stMetricValue"] {

    color: #f8fafc;
}


/* ============================================================
   SELECT BOX
   ============================================================ */

div[data-baseweb="select"] > div {

    background-color: #0d141f;

    border-color: #273448;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"] > div {

    background-color: #0d141f;
}


div[data-baseweb="textarea"] > div {

    background-color: #0d141f;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    border-radius: 8px;

    font-weight: 700;

    min-height: 2.5rem;
}


/* ============================================================
   INCIDENT
   ============================================================ */

.incident-title {

    color: #f8fafc;

    font-size: 1.2rem;

    font-weight: 750;
}


.incident-meta {

    color: #718096;

    font-size: 0.76rem;
}


/* ============================================================
   ROOT CAUSE
   ============================================================ */

.root-cause {

    background-color: #160e11;

    border: 1px solid #65282f;

    border-left: 4px solid #ef4444;

    border-radius: 12px;

    padding: 1.25rem 1.4rem;

    margin-top: 0.5rem;
}


.root-cause-label {

    color: #f87171;

    font-size: 0.67rem;

    font-weight: 800;

    letter-spacing: 0.13em;
}


.root-cause-text {

    color: #f8fafc;

    font-size: 1.12rem;

    font-weight: 650;

    line-height: 1.55;

    margin-top: 0.5rem;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    margin-top: 3rem;

    padding-top: 1rem;

    border-top: 1px solid #1d2635;

    text-align: center;

    color: #475569;

    font-size: 0.68rem;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {

    font-size: 0.78rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# CREATE ANALYZER
# ============================================================

@st.cache_resource
def create_analyzer():

    validate_config()

    return KubernetesAnalyzer()


try:

    analyzer = create_analyzer()

    analyzer_initialized = True

    st.session_state.connection_error = None

except Exception as exc:

    analyzer_initialized = False

    st.session_state.connection_error = str(exc)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## WORKSPACE"
    )


    namespace = st.text_input(
        "Kubernetes Namespace",
        value=st.session_state.namespace,
    ).strip()


    if not namespace:

        namespace = "monitoring"


    st.divider()


    st.markdown(
        "### CLUSTER"
    )

    st.caption(
        "Provider"
    )

    st.write(
        "IBM Cloud IKS"
    )

    st.caption(
        "Context"
    )

    st.write(
        "Kubernetes"
    )


    st.divider()


    st.markdown(
        "### DIAGNOSTIC MODE"
    )

    st.write(
        "🔒 Read-only"
    )


    st.divider()


    st.markdown(
        "### AI PIPELINE"
    )

    st.write(
        "Kubernetes API"
    )

    st.caption("↓")

    st.write(
        "Evidence Collection"
    )

    st.caption("↓")

    st.write(
        "Diagnostic Engine"
    )

    st.caption("↓")

    st.write(
        "LangChain"
    )

    st.caption("↓")

    st.write(
        "OpenAI"
    )

    st.caption("↓")

    st.write(
        "Root Cause Analysis"
    )


# ============================================================
# RESET WHEN NAMESPACE CHANGES
# ============================================================

if namespace != st.session_state.namespace:

    st.session_state.namespace = namespace

    st.session_state.pods = []

    st.session_state.analysis_result = None

    st.session_state.selected_pod = None


# ============================================================
# APPLICATION HEADER
# ============================================================

header_left, header_right = st.columns(
    [7, 1],
    vertical_alignment="center",
)


with header_left:

    st.markdown(
        '<div class="header-title">'
        '⚡ K8s AI Doctor'
        '</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        f'<div class="header-subtitle">'
        f'Kubernetes Incident Intelligence '
        f'· Namespace: <b>{namespace}</b>'
        f'</div>',
        unsafe_allow_html=True,
    )


with header_right:

    if analyzer_initialized:

        st.markdown(
            '<div class="header-status header-online">'
            '● IKS CONNECTED'
            '</div>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            '<div class="header-status header-offline">'
            '● CONNECTION ERROR'
            '</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# INITIALIZATION ERROR
# ============================================================

if not analyzer_initialized:

    st.error(
        "Kubernetes client initialization failed."
    )

    st.code(
        st.session_state.connection_error
    )

    st.stop()


# ============================================================
# SYNC CLUSTER
# ============================================================

sync_col, spacer_col = st.columns(
    [1, 7]
)


with sync_col:

    refresh = st.button(
        "↻ Sync Cluster",
        use_container_width=True,
    )


# ============================================================
# FETCH PODS
# ============================================================

if refresh or not st.session_state.pods:

    with st.spinner(
        "Synchronizing Kubernetes cluster..."
    ):

        try:

            st.session_state.pods = (
                analyzer.kubernetes.get_pods(
                    namespace
                )
            )

            st.session_state.connection_error = None

        except Exception as exc:

            st.session_state.connection_error = str(
                exc
            )

            st.session_state.pods = []


# ============================================================
# KUBERNETES ERROR
# ============================================================

if st.session_state.connection_error:

    st.error(
        "Unable to retrieve Kubernetes resources."
    )

    st.code(
        st.session_state.connection_error
    )

    st.info(
        "Verify that kubectl is authenticated against "
        "your IKS cluster and that the Python Kubernetes "
        "client is using the same kubeconfig."
    )

    st.stop()


# ============================================================
# PODS
# ============================================================

pods = st.session_state.pods


if not pods:

    st.info(
        f"No workloads found in namespace `{namespace}`."
    )

    st.stop()


# ============================================================
# HEALTH CALCULATION
# ============================================================

healthy_statuses = {
    "Running",
    "Succeeded",
}


healthy = [
    pod
    for pod in pods
    if pod.get("status")
    in healthy_statuses
]


attention = [
    pod
    for pod in pods
    if pod.get("status")
    not in healthy_statuses
]


critical = [
    pod
    for pod in pods
    if pod.get("status")
    not in {
        "Running",
        "Succeeded",
        "Pending",
    }
]


# ============================================================
# CLUSTER HEALTH
# ============================================================

st.markdown(
    '<div class="section-label">'
    'CLUSTER HEALTH'
    '</div>',
    unsafe_allow_html=True,
)


metric1, metric2, metric3, metric4 = st.columns(
    4
)


with metric1:

    st.metric(
        "WORKLOADS",
        len(pods),
    )


with metric2:

    st.metric(
        "HEALTHY",
        len(healthy),
    )


with metric3:

    st.metric(
        "ATTENTION",
        len(attention),
    )


with metric4:

    st.metric(
        "CRITICAL",
        len(critical),
    )


# ============================================================
# ACTIVE INCIDENTS
# ============================================================

problematic = [
    pod
    for pod in pods
    if pod.get("status")
    not in healthy_statuses
]


if not problematic:

    st.success(
        "✓ All workloads are healthy."
    )

    st.stop()


st.markdown(
    '<div class="section-label">'
    'ACTIVE INCIDENTS'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# INCIDENT SELECTOR
# ============================================================

incident_labels = []


for pod in problematic:

    pod_name = pod.get(
        "name",
        "Unknown",
    )

    status = pod.get(
        "status",
        "Unknown",
    )


    icon = (
        "🟡"
        if status == "Pending"
        else "🔴"
    )


    incident_labels.append(
        f"{icon} {pod_name} · {status}"
    )


selected_label = st.selectbox(
    "Select incident",
    incident_labels,
    label_visibility="collapsed",
)


selected_index = incident_labels.index(
    selected_label
)


selected_pod = problematic[
    selected_index
]


st.session_state.selected_pod = selected_pod


# ============================================================
# INCIDENT DETAILS
# ============================================================

status = selected_pod.get(
    "status",
    "Unknown",
)

pod_name = selected_pod.get(
    "name",
    "Unknown",
)

pod_phase = selected_pod.get(
    "phase",
    "Unknown",
)

node_name = selected_pod.get(
    "node_name"
)


st.markdown(
    '<div class="section-label">'
    'INCIDENT DETAILS'
    '</div>',
    unsafe_allow_html=True,
)


if status == "Pending":

    st.warning(
        f"⚠️ WARNING · {pod_name}"
    )

elif status in {
    "ImagePullBackOff",
    "ErrImagePull",
    "CrashLoopBackOff",
    "OOMKilled",
}:

    st.error(
        f"🔴 CRITICAL · {pod_name}"
    )

else:

    st.info(
        f"ℹ️ {status} · {pod_name}"
    )


meta1, meta2, meta3, meta4 = st.columns(
    4
)


with meta1:

    st.caption(
        "NAMESPACE"
    )

    st.write(
        namespace
    )


with meta2:

    st.caption(
        "STATUS"
    )

    st.write(
        status
    )


with meta3:

    st.caption(
        "PHASE"
    )

    st.write(
        pod_phase
    )


with meta4:

    st.caption(
        "NODE"
    )

    st.write(
        node_name
        if node_name
        else "Unassigned"
    )


# ============================================================
# ENGINEER OBSERVATION
# ============================================================

st.markdown(
    '<div class="section-label">'
    'ENGINEER OBSERVATION'
    '</div>',
    unsafe_allow_html=True,
)


observation = st.text_area(
    "Additional context",
    placeholder=(
        "Example: Prometheus pods started failing "
        "after a network configuration change."
    ),
    height=90,
    label_visibility="collapsed",
)


# ============================================================
# ACTION BUTTONS
# ============================================================

analyze_col, refresh_col = st.columns(
    [5, 1]
)


with analyze_col:

    analyze = st.button(
        "🔍 Investigate Incident",
        type="primary",
        use_container_width=True,
    )


with refresh_col:

    quick_refresh = st.button(
        "↻",
        use_container_width=True,
    )


if quick_refresh:

    st.session_state.pods = []

    st.session_state.analysis_result = None

    st.rerun()


# ============================================================
# AI INVESTIGATION
# ============================================================

if analyze:

    with st.spinner(
        "Collecting Kubernetes evidence and "
        "performing AI investigation..."
    ):

        try:

            result = analyzer.analyze_pod(
                namespace=namespace,
                pod_name=selected_pod["name"],
            )

            st.session_state.analysis_result = result

        except Exception as exc:

            st.error(
                f"AI investigation failed: {exc}"
            )


# ============================================================
# AI ROOT CAUSE ANALYSIS
# ============================================================

result = st.session_state.analysis_result


if result:

    st.divider()


    st.markdown(
        '<div class="section-label">'
        'AI ROOT CAUSE ANALYSIS'
        '</div>',
        unsafe_allow_html=True,
    )


    # ========================================================
    # ROOT CAUSE
    # ========================================================

    root_cause_html = (
        '<div class="root-cause">'
        '<div class="root-cause-label">'
        'MOST LIKELY ROOT CAUSE'
        '</div>'
        '<div class="root-cause-text">'
        f'{result.root_cause}'
        '</div>'
        '</div>'
    )


    st.markdown(
        root_cause_html,
        unsafe_allow_html=True,
    )


    # ========================================================
    # CONFIDENCE
    # ========================================================

    confidence = str(
        result.confidence
    ).strip().upper()


    if confidence == "HIGH":

        st.success(
            "🎯 HIGH CONFIDENCE — "
            "The available Kubernetes evidence strongly "
            "supports this diagnosis."
        )

    elif confidence == "MEDIUM":

        st.warning(
            "🎯 MEDIUM CONFIDENCE — "
            "Additional investigation is recommended."
        )

    else:

        st.error(
            "🎯 LOW CONFIDENCE — "
            "The available evidence is insufficient."
        )


    # ========================================================
    # WHY THIS HAPPENED + EVIDENCE
    # ========================================================

    why_col, evidence_col = st.columns(
        [1.25, 1]
    )


    with why_col:

        st.markdown(
            '<div class="section-label">'
            'WHY THIS HAPPENED'
            '</div>',
            unsafe_allow_html=True,
        )


        with st.container(
            border=True
        ):

            st.write(
                result.why_this_is_happening
            )


    with evidence_col:

        st.markdown(
            '<div class="section-label">'
            'KEY EVIDENCE'
            '</div>',
            unsafe_allow_html=True,
        )


        evidence = (
            result.evidence or []
        )


        if evidence:

            for item in evidence:

                st.info(
                    f"● {item}"
                )

        else:

            st.caption(
                "No evidence returned."
            )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    st.markdown(
        '<div class="section-label">'
        'RECOMMENDED INVESTIGATION'
        '</div>',
        unsafe_allow_html=True,
    )


    recommendations = (
        result.recommended_investigation
        or []
    )


    if recommendations:

        for index, recommendation in enumerate(
            recommendations,
            start=1,
        ):

            st.write(
                f"**{index:02d}.** {recommendation}"
            )

    else:

        st.caption(
            "No recommendations returned."
        )


    # ========================================================
    # SAFE KUBECTL COMMANDS
    # ========================================================

    st.markdown(
        '<div class="section-label">'
        'SAFE KUBECTL COMMANDS'
        '</div>',
        unsafe_allow_html=True,
    )


    commands = (
        result.safe_kubectl_commands
        or []
    )


    if commands:

        command_col1, command_col2 = st.columns(
            2
        )


        for index, command in enumerate(
            commands
        ):

            with (
                command_col1
                if index % 2 == 0
                else command_col2
            ):

                st.code(
                    command,
                    language="bash",
                )

    else:

        st.caption(
            "No diagnostic commands returned."
        )


    # ========================================================
    # TECHNICAL DETAILS
    # ========================================================

    st.markdown(
        '<div class="section-label">'
        'TECHNICAL DETAILS'
        '</div>',
        unsafe_allow_html=True,
    )


    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Evidence",
            "Kubernetes",
            "AI Analysis",
            "Commands",
        ]
    )


    # ========================================================
    # EVIDENCE TAB
    # ========================================================

    with tab1:

        st.subheader(
            "Observed Facts"
        )


        facts = (
            result.observed_facts
            or []
        )


        if facts:

            for fact in facts:

                st.write(
                    f"✓ {fact}"
                )

        else:

            st.caption(
                "No observed facts returned."
            )


        st.divider()


        st.subheader(
            "Evidence"
        )


        for item in (
            result.evidence or []
        ):

            st.write(
                f"• {item}"
            )


    # ========================================================
    # KUBERNETES TAB
    # ========================================================

    with tab2:

        st.json(
            {
                "namespace": namespace,
                "pod": selected_pod,
            }
        )


    # ========================================================
    # AI ANALYSIS TAB
    # ========================================================

    with tab3:

        st.subheader(
            "Incident"
        )

        st.write(
            result.incident
        )


        st.subheader(
            "Root Cause"
        )

        st.write(
            result.root_cause
        )


        st.subheader(
            "Reasoning"
        )

        st.write(
            result.why_this_is_happening
        )


        st.subheader(
            "Confidence"
        )

        st.write(
            result.confidence
        )


    # ========================================================
    # COMMANDS TAB
    # ========================================================

    with tab4:

        commands = (
            result.safe_kubectl_commands
            or []
        )


        if commands:

            for command in commands:

                st.code(
                    command,
                    language="bash",
                )

        else:

            st.caption(
                "No commands returned."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'K8s AI Doctor · Kubernetes Incident Intelligence '
    '· IBM Cloud IKS · LangChain · OpenAI · LangSmith '
    '· Read-only diagnostics'
    '</div>',
    unsafe_allow_html=True,
)