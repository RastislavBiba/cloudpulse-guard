# NOTIX SRE Runbook RB-202: Kubernetes Pod Hardening Policy
## Postihnuté komponenty: K8s Deployment, Pod, DaemonSet

### Bezpečnostné pravidlá (CIS Benchmark):
1. Žiadny kontajner nesmie bežať pod rootom (`runAsUser: 0` je zakázané). Povinné je `runAsNonRoot: true` a UID >= 10001.
2. `privileged: true` je prísne zakázané v celom produkčnom klastri AKS.
3. Každý kontajner MUSÍ mať nastavené `readOnlyRootFilesystem: true`.
4. Všetky capabilities musia byť dropnuté (`drop: ["ALL"]`).
