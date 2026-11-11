# NOTIX SRE Runbook RB-303: Terraform Security Group Compliance
## Postihnuté komponenty: aws_security_group, azurerm_network_security_group

### Politika otvorenosti:
1. Ingress pravidlá s `0.0.0.0/0` a portom `-1` (all traffic) sú okamžite klasifikované ako CRITICAL FAIL.
2. Povolené verejné porty sú výlučne 80 a 443 na Load Balanceri, nikdy nie priamo na backend inštanciách.
