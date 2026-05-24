from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CertificatePaths:
    output_dir: Path
    ca_key: Path
    ca_cert: Path
    server_key: Path
    server_csr: Path
    server_cert: Path
    server_ext: Path


def run_openssl(args: list[str]) -> None:
    subprocess.run(["openssl", *args], check=True, capture_output=True, text=True)


def generate_localhost_certificates(output_dir: Path, days: int = 7) -> CertificatePaths:
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = CertificatePaths(
        output_dir=output_dir,
        ca_key=output_dir / "lab-ca.key",
        ca_cert=output_dir / "lab-ca.crt",
        server_key=output_dir / "localhost.key",
        server_csr=output_dir / "localhost.csr",
        server_cert=output_dir / "localhost.crt",
        server_ext=output_dir / "localhost.ext",
    )

    paths.server_ext.write_text(
        "\n".join(
            [
                "authorityKeyIdentifier=keyid,issuer",
                "basicConstraints=CA:FALSE",
                "keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment",
                "subjectAltName = @alt_names",
                "",
                "[alt_names]",
                "DNS.1 = localhost",
                "IP.1 = 127.0.0.1",
                "",
            ]
        ),
        encoding="utf-8",
    )

    run_openssl(
        [
            "req",
            "-x509",
            "-newkey",
            "rsa:2048",
            "-sha256",
            "-days",
            str(days),
            "-nodes",
            "-subj",
            "/CN=IPOG Lab Local CA",
            "-keyout",
            str(paths.ca_key),
            "-out",
            str(paths.ca_cert),
        ]
    )
    run_openssl(
        [
            "req",
            "-newkey",
            "rsa:2048",
            "-nodes",
            "-subj",
            "/CN=localhost",
            "-keyout",
            str(paths.server_key),
            "-out",
            str(paths.server_csr),
        ]
    )
    run_openssl(
        [
            "x509",
            "-req",
            "-in",
            str(paths.server_csr),
            "-CA",
            str(paths.ca_cert),
            "-CAkey",
            str(paths.ca_key),
            "-CAcreateserial",
            "-out",
            str(paths.server_cert),
            "-days",
            str(days),
            "-sha256",
            "-extfile",
            str(paths.server_ext),
        ]
    )
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera uma CA local e certificado TLS para localhost.")
    parser.add_argument("--output-dir", default="certs", help="Diretorio de saida dos certificados.")
    parser.add_argument("--days", type=int, default=7, help="Validade dos certificados em dias.")
    args = parser.parse_args()

    paths = generate_localhost_certificates(Path(args.output_dir), days=args.days)
    print(f"CA local: {paths.ca_cert}")
    print(f"Certificado do servidor: {paths.server_cert}")
    print(f"Chave do servidor: {paths.server_key}")


if __name__ == "__main__":
    main()
