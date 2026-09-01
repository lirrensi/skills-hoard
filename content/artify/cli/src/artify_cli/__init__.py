"""artify_cli - standalone HTML artifact preview/serve/snapshot CLI.

A dependency-declaring, self-contained Click CLI for the ``artify`` skill.
Run it with ``uv run --project artify/cli artify ...`` — uv resolves the
declared requirements into a throwaway environment on the fly. No global
install required.
"""

from artify_cli.cli import main

__all__ = ["main"]
__version__ = "0.0.0"
