import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY"
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini",
)

LANGSMITH_TRACING = os.getenv(
    "LANGSMITH_TRACING",
    "true",
)

LANGSMITH_API_KEY = os.getenv(
    "LANGSMITH_API_KEY"
)

LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "k8s-ai-troubleshooter",
)


def validate_config():

    missing = []

    if not OPENAI_API_KEY:

        missing.append(
            "OPENAI_API_KEY"
        )

    if not LANGSMITH_API_KEY:

        missing.append(
            "LANGSMITH_API_KEY"
        )

    if missing:

        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )