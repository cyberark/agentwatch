import os
import sys
from multiprocessing import current_process

from agentwatch.consts import AGENTWATCH_INTERNAL
from agentwatch.core import initialize


def _is_direct_execution() -> bool:
    return sys.argv[0].endswith("agentwatch")

def _safe_to_start() -> bool:
    # Only run on original script execution, not in subprocess or interpreter bootstrapping
    return current_process().name == "MainProcess" \
        and not hasattr(sys, '_called_from_spawn') \
        and os.environ.get(AGENTWATCH_INTERNAL) is None \
        and "PYTEST_VERSION" not in os.environ \
        and not _is_direct_execution()

if _safe_to_start():
    initialize()