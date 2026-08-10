# Sanitization and Privacy Protection
This document describes the sanitization methodology at a conceptual level.
Implementation details such as hashing salts and internal mappings are not disclosed.

The public dataset is derived from internal telemetry archives using a deterministic sanitization pipeline designed to ensure privacy, security, and compliance with institutional data governance policies.

## Identifier Pseudonymization
The following identifiers are replaced using salted SHA-256 hashing:
- node hostnames
- GPU UUIDs
- Prometheus instance labels

The mapping table and hashing salt are retained internally and are not included in the public dataset.
Pseudonymized identifiers remain consistent across files to preserve temporal and structural relationships.

## Removal of Environment References
All environment-specific information is removed, including:
- absolute filesystem paths
- local system references
- infrastructure-specific identifiers

This ensures that no internal deployment details can be inferred from the dataset.

## Sensitive Pattern Scanning
All textual fields are systematically scanned for sensitive patterns, including:
- IP addresses
- URLs
- email addresses
- filesystem paths
- access tokens or credentials

Detected patterns are removed or replaced to eliminate potential leakage of sensitive information.

## Field Minimization
Only telemetry necessary for the study is retained. The dataset includes:
- timestamps (UTC)
- metric names and values
- pseudonymized identifiers
- monitoring and scheduler signals

The dataset explicitly excludes:
- user data
- job-level workload information
- application-specific data
- credentials or authentication artifacts

## Residual Risk
The dataset contains operational telemetry only and does not expose:
- personal data
- credentials
- network information
- system topology

Given the applied sanitization procedures, the residual risk of sensitive information disclosure is considered minimal.

## Compliance Statement
This dataset complies with institutional data protection and publication policies.
All included data has been processed to remove or anonymize sensitive content and is suitable for public release and research use.

## Institutional Approval
This dataset has been prepared and released in accordance with the data governance and publication policies of the GWDG HPC infrastructure.
The dataset was reviewed prior to publication to ensure compliance with privacy, security, and operational constraints.
Only sanitized telemetry suitable for public research use is included.
