def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="cs">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NOTIX s.r.o. | CloudPulse Guard & LLMOps</title>
    <style>
        :root {
            --bg: #0b1120;
            --card-bg: #151f32;
            --border: #233554;
            --cyan: #00e5ff;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --danger: #f87171;
            --warning: #fbbf24;
            --success: #34d399;
            --purple: #c084fc;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: var(--bg);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.5;
            padding: 2rem 1rem;
        }
        .container { max-width: 1050px; margin: 0 auto; }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .brand-box { display: flex; align-items: center; gap: 0.85rem; }
        .logo-badge {
            width: 44px;
            height: 44px;
            background: linear-gradient(135deg, #00e5ff, #0077b6);
            color: #0b1120;
            font-weight: 900;
            font-size: 1.4rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            box-shadow: 0 4px 14px rgba(0, 229, 255, 0.25);
        }
        .brand-title { font-size: 1.5rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem; }
        .brand-tag {
            font-size: 0.7rem;
            background: rgba(0, 229, 255, 0.1);
            color: var(--cyan);
            border: 1px solid rgba(0, 229, 255, 0.3);
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
        }
        .subtitle { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem; }
        .live-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(52, 211, 153, 0.1);
            border: 1px solid rgba(52, 211, 153, 0.3);
            color: var(--success);
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.4rem 0.8rem;
            border-radius: 9999px;
        }
        .live-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 8px var(--success);
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
        }
        .input-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .label { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; }
        .chips-group { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }
        .chips-label { font-size: 0.75rem; color: var(--text-muted); }
        .chip-btn {
            background: #0f172a;
            border: 1px solid var(--border);
            color: var(--cyan);
            font-size: 0.75rem;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .chip-btn:hover { background: var(--border); color: #fff; }
        textarea {
            width: 100%;
            background: #070b14;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1rem;
            font-family: ui-monospace, Menlo, Consolas, monospace;
            font-size: 0.8rem;
            color: var(--cyan);
            outline: none;
            resize: vertical;
        }
        textarea:focus { border-color: var(--cyan); }
        .input-bottom {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1rem;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .helper-text { font-size: 0.75rem; color: var(--text-muted); }
        .submit-btn {
            background: linear-gradient(135deg, var(--cyan), #0077b6);
            color: #0b1120;
            font-weight: 800;
            font-size: 0.9rem;
            padding: 0.75rem 1.6rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(0, 229, 255, 0.3);
        }
        .submit-btn:hover { filter: brightness(1.1); }
        #loader { text-align: center; padding: 3rem 0; display: none; }
        .spinner {
            display: inline-block;
            width: 42px;
            height: 42px;
            border: 4px solid rgba(0, 229, 255, 0.2);
            border-top-color: var(--cyan);
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .loader-text { margin-top: 1rem; font-size: 0.85rem; color: var(--text-muted); }

        #results { display: none; margin-bottom: 2rem; }
        .llmops-bar {
            background: rgba(15, 23, 42, 0.7);
            border: 1px dashed var(--purple);
            border-radius: 12px;
            padding: 0.85rem 1.25rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        .llmops-item { font-size: 0.8rem; color: var(--text-muted); }
        .llmops-val { font-weight: 800; color: var(--purple); font-family: ui-monospace, monospace; }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem;
        }
        .metric-title { font-size: 0.7rem; font-weight: 700; color: var(--text-muted); letter-spacing: 0.05em; }
        .metric-value { font-size: 1.2rem; font-weight: 800; margin-top: 0.3rem; }
        .two-cols {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .detail-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }
        .card-title { font-size: 0.9rem; font-weight: 700; color: #fff; }
        .copy-btn {
            background: #0f172a;
            border: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 0.7rem;
            padding: 0.25rem 0.5rem;
            border-radius: 5px;
            cursor: pointer;
        }
        .code-block {
            background: #070b14;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.85rem;
            font-family: ui-monospace, Menlo, Consolas, monospace;
            font-size: 0.8rem;
            color: var(--warning);
            overflow-x: auto;
            max-height: 250px;
        }
        .client-card {
            background: linear-gradient(145deg, #151f32, #0d1527);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 1.25rem;
        }
        .summary-text { font-size: 0.9rem; font-style: italic; color: #cbd5e1; margin-top: 0.5rem; }
        footer {
            border-top: 1px solid var(--border);
            padding-top: 1.5rem;
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-muted);
            flex-wrap: wrap;
            gap: 0.5rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <div class="brand-box">
                <div class="logo-badge">N</div>
                <div>
                    <div class="brand-title">
                        NOTIX <span class="brand-tag">s.r.o.</span>
                        <span style="color: var(--border); font-weight: 300;">|</span>
                        <span style="font-size: 1.15rem; color: #cbd5e1;">CloudPulse Guard & LLMOps</span>
                    </div>
                    <div class="subtitle">Enterprise IaC Security, K8s Compliance & Azure AI Foundry Auditor</div>
                </div>
            </div>
            <div class="live-badge">
                <span class="live-dot"></span> Azure AI Foundry Connected
            </div>
        </header>

        <div class="card">
            <div class="input-top">
                <span class="label">Vstup incidentu / kódu:</span>
                <div class="chips-group">
                    <span class="chips-label">Rýchle šablóny:</span>
                    <button type="button" class="chip-btn" onclick="setScenario('cef')">CEF Security Gateway</button>
                    <button type="button" class="chip-btn" onclick="setScenario('k8s')">K8s Root Pod</button>
                    <button type="button" class="chip-btn" onclick="setScenario('docker')">Dockerfile Leak</button>
                    <button type="button" class="chip-btn" onclick="setScenario('tf')">Terraform Open SG</button>
                </div>
            </div>

            <textarea id="logInput" rows="7" placeholder="Sem vložte CEF log, YAML manifest, Dockerfile alebo Terraform konfiguráciu..."></textarea>

            <div class="input-bottom">
                <span class="helper-text">⚡ Azure AI Foundry (gpt-5-mini) • Policy & Incident Audit</span>
                <button id="runBtn" class="submit-btn" onclick="analyzeLog()">Analyzovať & Auditovať</button>
            </div>
        </div>

        <div id="loader">
            <div class="spinner"></div>
            <div class="loader-text">CloudPulse Guard analyzuje požiadavku a počíta metriky...</div>
        </div>

        <div id="results">
            <div class="llmops-bar">
                <div class="llmops-item">⏱️ Latencia: <span id="resLatency" class="llmops-val">0.0s</span></div>
                <div class="llmops-item">📊 Spotreba tokenov: <span id="resTokens" class="llmops-val">0</span> (vstup: <span id="resInTokens">0</span>, výstup: <span id="resOutTokens">0</span>)</div>
                <div class="llmops-item">💰 Cena auditu: <span id="resCost" class="llmops-val">$0.000000</span></div>
                <div class="llmops-item">🤖 Model: <span id="resModel" class="llmops-val">gpt-5-mini</span></div>
            </div>

            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-title">ZÁVAŽNOSŤ</div>
                    <div id="resSeverity" class="metric-value" style="color: var(--danger);">CRITICAL</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">COMPLIANCE / HEALTH</div>
                    <div id="resCategory" class="metric-value" style="color: var(--cyan); font-size: 1.2rem;">0 / 100</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">POČET RIZÍK</div>
                    <div id="resSla" class="metric-value" style="color: var(--warning);">0 Nálezov</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">BEZPEČNOSTNÝ VERDIKT</div>
                    <div id="resSafety" class="metric-value" style="color: var(--success);">AUDITED</div>
                </div>
            </div>

            <div class="two-cols">
                <div class="detail-card">
                    <div>
                        <div class="card-header">
                            <span class="card-title">🔍 Bezpečnostné & Prevádzkové nálezy</span>
                            <span id="resComponent" style="font-size: 0.75rem; background: #0f172a; padding: 0.2rem 0.5rem; border-radius: 4px; font-family: monospace;"></span>
                        </div>
                        <div id="resRootCause" style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; max-height: 250px; overflow-y: auto;"></div>
                    </div>
                </div>

                <div class="detail-card">
                    <div>
                        <div class="card-header">
                            <span class="card-title">⚙️ Auto-Remediation / Runbook</span>
                            <button class="copy-btn" onclick="copyCode()">Kopírovať</button>
                        </div>
                        <div class="code-block"><code id="resCmd"></code></div>
                    </div>
                </div>
            </div>

            <div class="client-card">
                <div class="card-header">
                    <span class="card-title">📋 NOTIX Klientsky & Ticket Súhrn (SRE Report)</span>
                    <button class="copy-btn" onclick="copySummary()">Kopírovať report</button>
                </div>
                <p id="resSummary" class="summary-text"></p>
            </div>
        </div>

        <footer>
            <div>Navrhnuté pre podnikovú infraštruktúru a konzultácie <strong style="color: #fff;">NOTIX s.r.o.</strong></div>
            <div>Kubernetes • Azure AI Foundry • GitHub Actions CI/CD</div>
        </footer>
    </div>

    <script>
        let currentType = 'cef_log';

        function setScenario(type) {
            currentType = type;
            if (type === 'cef') {
                currentType = 'cef_log';
                document.getElementById('logInput').value = 'CEF:1|Notix|security-gateway|2.1.0|||8| rt=Nov 03 2026 14:21:11.128 UTC cs1Label=ApplicationName cs1=security-gateway cs2Label=Class.Method cs2=c.m.p.b.c.e.h.LastExceptionHandler.handleForbidden cs3Label=ExceptionType cs3=WebClientRequestException cs4Label=Thread cs4=https-jsse-nio-8443-exec-8 cs5Label=RequestUrl cs5=/auth/login cs6Label=Msg cs6=connection timed out after 30000 ms: auth.cms.gov.cz/94.199.44.157:443 flexString1Label=SID flexString1=';
            } else if (type === 'k8s') {
                currentType = 'kubernetes';
                document.getElementById('logInput').value = `apiVersion: v1
kind: Pod
metadata:
  name: insecure-api-pod
spec:
  containers:
  - name: backend
    image: nginx:latest
    securityContext:
      privileged: true
      runAsUser: 0
    ports:
    - containerPort: 80`;
            } else if (type === 'docker') {
                currentType = 'dockerfile';
                document.getElementById('logInput').value = `FROM ubuntu:latest
ENV DB_PASSWORD="SuperSecretProductionPassword123!"
USER root
RUN apt-get update && apt-get install -y curl
CMD ["curl", "http://internal-db:5432"]`;
            } else {
                currentType = 'terraform';
                document.getElementById('logInput').value = `resource "aws_security_group" "allow_all" {
  name        = "open-production-sg"
  description = "Dangerous wide open ingress"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}`;
            }
        }

        async function analyzeLog() {
            const text = document.getElementById('logInput').value;
            if(!text || text.length < 5) {
                alert("Zadajte prosím platný vstup (aspoň 5 znakov).");
                return;
            }

            document.getElementById('loader').style.display = 'block';
            document.getElementById('results').style.display = 'none';

            try {
                const response = await fetch('/api/audit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code_snippet: text, code_type: currentType })
                });

                if(!response.ok) throw new Error("Chyba spracovania: " + response.statusText);
                const data = await response.json();

                // Bezpečné načítanie LLMOps metrík
                const latency = data.latency_seconds ?? data.llmops?.total_latency_seconds ?? 0;
                const totalTokens = data.total_tokens ?? data.llmops?.total_tokens ?? 0;
                const promptTokens = data.prompt_tokens ?? data.llmops?.total_prompt_tokens ?? 0;
                const completionTokens = data.completion_tokens ?? data.llmops?.total_output_tokens ?? 0;
                const cost = data.cost_usd ?? data.llmops?.estimated_cost_usd ?? 0;
                const model = data.model_used ?? "gpt-5-mini";

                document.getElementById('resLatency').innerText = Number(latency).toFixed(2) + "s";
                document.getElementById('resTokens').innerText = totalTokens;
                document.getElementById('resInTokens').innerText = promptTokens;
                document.getElementById('resOutTokens').innerText = completionTokens;
                document.getElementById('resCost').innerText = "$" + Number(cost).toFixed(6);
                document.getElementById('resModel').innerText = model;

                const sev = data.severity ?? "HIGH";
                document.getElementById('resSeverity').innerText = sev;
                document.getElementById('resSeverity').style.color = sev === 'CRITICAL' ? 'var(--danger)' : (sev === 'HIGH' ? 'var(--warning)' : 'var(--success)');
                
                const score = data.compliance_score ?? 50;
                document.getElementById('resCategory').innerText = score + " / 100";
                
                const findings = data.findings || [];
                document.getElementById('resSla').innerText = findings.length + " nálezov";
                document.getElementById('resSafety').innerText = score > 75 ? "PASSED" : "FAILED / RISK";
                document.getElementById('resSafety').style.color = score > 75 ? "var(--success)" : "var(--danger)";
                document.getElementById('resComponent').innerText = currentType.toUpperCase();

                const findingsContainer = document.getElementById('resRootCause');
                findingsContainer.innerHTML = '';
                findings.forEach(f => {
                    const row = document.createElement('div');
                    row.style.marginBottom = '0.75rem';
                    row.style.padding = '0.5rem 0.75rem';
                    row.style.background = '#070b14';
                    row.style.borderRadius = '6px';
                    row.style.borderLeft = '3px solid ' + (f.severity === 'CRITICAL' ? 'var(--danger)' : (f.severity === 'HIGH' ? 'var(--warning)' : 'var(--cyan)'));
                    row.innerHTML = `<b style="color: #fff; font-size: 0.8rem;">[${f.severity}] ${f.issue}</b><br><span style="font-size: 0.75rem; color: var(--text-muted);">${f.recommendation}</span>`;
                    findingsContainer.appendChild(row);
                });

                document.getElementById('resCmd').innerText = data.remediated_snippet || "# Bez zmeny";
                document.getElementById('resSummary').innerText = data.summary || "Audit dokončený.";

                document.getElementById('results').style.display = 'block';
            } catch(e) {
                alert("Chyba: " + e.message);
            } finally {
                document.getElementById('loader').style.display = 'none';
            }
        }

        function copyCode() {
            const code = document.getElementById('resCmd').innerText;
            navigator.clipboard.writeText(code);
            alert("Kód/príkaz bol skopírovaný do schránky!");
        }

        function copySummary() {
            const text = document.getElementById('resSummary').innerText;
            navigator.clipboard.writeText(text);
            alert("Report bol skopírovaný do schránky!");
        }
    </script>
</body>
</html>"""
