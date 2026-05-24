from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def openssl_output(args: list[str]) -> str:
    result = subprocess.run(["openssl", *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _extract_san(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "X509v3 Subject Alternative Name" in line and index + 1 < len(lines):
            return lines[index + 1].strip()
    return ""


def inspect_certificate(cert_path: Path) -> dict[str, str]:
    subject = openssl_output(["x509", "-in", str(cert_path), "-noout", "-subject"])
    issuer = openssl_output(["x509", "-in", str(cert_path), "-noout", "-issuer"])
    dates = openssl_output(["x509", "-in", str(cert_path), "-noout", "-dates"])
    text = openssl_output(["x509", "-in", str(cert_path), "-noout", "-text"])

    date_values = dict(line.split("=", 1) for line in dates.splitlines())
    return {
        "subject": subject.removeprefix("subject=").strip(),
        "issuer": issuer.removeprefix("issuer=").strip(),
        "not_before": date_values.get("notBefore", ""),
        "not_after": date_values.get("notAfter", ""),
        "subject_alternative_name": _extract_san(text),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspeciona campos principais de um certificado X.509.")
    parser.add_argument("certificate", help="Caminho do certificado .crt/.pem.")
    args = parser.parse_args()

    details = inspect_certificate(Path(args.certificate))
    for key, value in details.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
