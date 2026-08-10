# Dataset Description

## Overview
This dataset contains sanitized telemetry from GPU-equipped HPC nodes at GWDG,
aligned with GPU failure incidents.

The telemetry is extracted from Prometheus monitoring archives and converted
into tidy time-series tables with fixed sampling cadence.

## Telemetry Planes
### GPU telemetry (DCGM)
- utilization
- temperature
- power
- memory state
- clocks
- NVLink/PCIe indicators

### Node/OS telemetry
- CPU load
- memory availability
- paging activity
- OOM events

### Monitoring pipeline telemetry
- scrape duration
- scrape success
- sample counts
- series counts

### Scheduler state
- node state transitions (ALLOC, IDLE, DRAIN, DOWN)

## Temporal Alignment
Each incident is represented with:
- incident time
- collection start
- collection end
- pre-incident window
- post-incident window

## Sampling
Telemetry cadence: 10-minute or 15-minute intervals  
Time column: UTC

## Tidy Format
Each row represents:
(timeUtc, node, metric, value, labels…)

## Identifiers
- node: pseudonymized HPC node identifier  
- uuid: pseudonymized GPU identifier  
- instance: pseudonymized exporter instance  

Identifiers are stable across files.

## Limitations
- No workload/application context
- No topology or rack information
- No scheduler job metadata
- No user information

## Dataset Scope

Time range: January 2025 to February 2026  
Sampling interval: 10–15 minutes  
Data type: Multivariate time-series telemetry  
Failure focus: GPU detachment and observability degradation events
