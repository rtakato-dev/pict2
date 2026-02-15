import pathlib
import subprocess


def test_1():
    output = "tests/output.txt"
    cmd = ["python", "-m", "pict2", "tests/test_model.pict", "-f", output]

    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    assert (
        pathlib.Path(output).read_text()
        == pathlib.Path("tests/expected_output.txt").read_text()
    ), "Output file is correct"


def test_2():
    output = "tests/output2.txt"
    cmd = ["python", "-m", "pict2", "tests/test_model.pict", "-f", output, "-o", "2"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, f"Command failed with error: {result.stderr}"
    assert (
        pathlib.Path(output).read_text()
        == pathlib.Path("tests/expected_output2.txt").read_text()
    ), "Output file is correct"
