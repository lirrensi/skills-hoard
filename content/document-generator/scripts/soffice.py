"""LibreOffice wrapper for document conversion.

Usage:
    python scripts/soffice.py --headless --convert-to pdf input.docx
    python scripts/soffice.py --headless --convert-to xlsx input.csv
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def get_soffice_env():
    """Get environment with LibreOffice paths."""
    env = os.environ.copy()
    if sys.platform == "win32":
        # Common LibreOffice paths on Windows
        paths = [
            r"C:\Program Files\LibreOffice\program",
            r"C:\Program Files (x86)\LibreOffice\program",
        ]
        current = env.get("PATH", "")
        for p in paths:
            if Path(p).exists():
                env["PATH"] = p + os.pathsep + current
                break
    return env


def convert(
    input_file: str,
    output_format: str,
    headless: bool = True,
) -> tuple[None, str]:
    """Convert file using LibreOffice."""
    input_path = Path(input_file)

    if not input_path.exists():
        return None, f"Error: {input_file} does not exist"

    cmd = ["soffice"]
    if headless:
        cmd.append("--headless")
    cmd.extend(["--convert-to", output_format, "--outdir", str(input_path.parent)])
    cmd.append(str(input_path))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=get_soffice_env(),
            timeout=60,
        )

        if result.returncode != 0:
            return None, f"Error: {result.stderr or 'Conversion failed'}"

        output_name = input_path.stem + "." + output_format
        output_path = input_path.parent / output_name

        return None, str(output_path)

    except subprocess.TimeoutExpired:
        return None, "Error: Conversion timed out"
    except Exception as e:
        return None, f"Error: {e}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LibreOffice document conversion")
    parser.add_argument(
        "--headless", action="store_true", default=True, help="Run headless"
    )
    parser.add_argument(
        "--convert-to", required=True, help="Target format (pdf, docx, xlsx, etc.)"
    )
    parser.add_argument("--outdir", help="Output directory")
    parser.add_argument("input_file", help="Input file")

    args = parser.parse_args()

    if args.outdir:
        os.chdir(args.outdir)

    _, message = convert(args.input_file, args.convert_to, args.headless)
    print(message)

    if message and message.startswith("Error"):
        sys.exit(1)
