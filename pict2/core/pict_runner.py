import subprocess
import sys
from pathlib import Path


class PictRunner:
    def __init__(self, pict_path: Path | None = None):
        if pict_path is None:
            if getattr(sys, "frozen", False):
                # If the application is frozen (e.g., by PyInstaller), use the executable's directory
                pict_path = Path(sys._MEIPASS) / "pict.exe"
            else:
                pict_path = Path(__file__).resolve().parent / "pict.exe"

        self.pict_path = pict_path

        if not self.pict_path.exists():
            raise FileNotFoundError(f"pict.exe not found: {self.pict_path}")

    def run(
        self,
        model_path: Path,
        pict_options: list[str] | None = None,
        output_path: Path | None = None,
    ) -> str:
        if pict_options is None:
            pict_options = []

        if not model_path.exists():
            raise FileNotFoundError(f"model file not found: {model_path}")

        cmd = [
            str(self.pict_path),
            str(model_path),
            *pict_options,
        ]

        if output_path:
            with output_path.open("w", encoding="utf-8", newline="") as f:
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                )
        else:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout or ""
