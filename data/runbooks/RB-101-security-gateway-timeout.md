# NOTIX SRE Runbook RB-101: Security Gateway Connection Timeout
## Postihnuté komponenty: security-gateway, Spring WebClient, /auth/login
## Kontext: auth.cms.gov.cz (Štátna integračná brána)

### Popis incidentu:
Ak dochádza k chybám WebClientRequestException a timeoutu (30000 ms) na auth.cms.gov.cz:443:
1. Výpadok je spôsobený buď expirovaným TLS certifikátom brány, alebo reštrikciou na Egress Firewall Pravidle (Port 443 TCP).
2. Štandardná hodnota 30s timeout blokuje worker thready (Tomcat/Nio).

### Povinné nápravné kroky NOTIX:
1. Okamžite znížiť connectionTimeout vo WebClient na 5000 ms.
2. Aktivovať Circuit Breaker (Resilience4j) so stavom HALF-OPEN po 3 zlyhaniach.
3. Spustiť overovací príkaz z bašty:
   `curl -Iv --connect-timeout 5 https://auth.cms.gov.cz:443/health`
4. Eskalovať na on-call L2 tím cez PagerDuty službu #sec-gateway.
