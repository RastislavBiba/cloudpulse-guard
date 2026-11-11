def get_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="cs" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudPulse Guard - SRE & Bezpečnostní Audit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 500: '#00d2ff', 600: '#0099cc' },
                        dark: { 900: '#0b0f19', 800: '#111827', 700: '#1f2937', 600: '#374151' }
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace']
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-dark-900 text-gray-200 font-sans min-h-screen flex flex-col antialiased">
    <!-- Horní navigační lišta -->
    <header class="border-b border-dark-700 bg-dark-800/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <span class="text-2xl font-black bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent">CloudPulse Guard</span>
                <span class="text-xs bg-dark-700 text-cyan-400 font-mono px-2 py-0.5 rounded border border-cyan-500/30">Azure AI Foundry</span>
            </div>
            <div class="flex items-center space-x-4 text-xs font-mono text-gray-400">
                <span class="flex items-center"><span class="w-2 h-2 rounded-full bg-emerald-500 mr-2 animate-pulse"></span>gpt-5-mini</span>
                <span class="text-gray-600">|</span>
                <span>NOTIX SRE & SecOps</span>
            </div>
        </div>
    </header>

    <!-- Hlavní obsah -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <!-- Vstupní karta -->
        <section class="bg-dark-800 border border-dark-700 rounded-xl p-6 shadow-xl">
            <div class="flex flex-wrap items-center justify-between gap-4 mb-4">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <span>Vstup incidentu / kódu:</span>
                    </h2>
                    <p class="text-xs text-gray-400">Podpora pro Kubernetes, Dockerfile, Terraform i CEF/Syslog záznamy</p>
                </div>
                <!-- Rychlé šablony -->
                <div class="flex flex-wrap items-center gap-2">
                    <span class="text-xs text-gray-500 font-mono">Rychlé šablony:</span>
                    <button onclick="setSample('cef')" class="text-xs bg-dark-700 hover:bg-dark-600 text-cyan-300 px-3 py-1.5 rounded-lg border border-cyan-500/30 transition">CEF Security Gateway</button>
                    <button onclick="setSample('k8s')" class="text-xs bg-dark-700 hover:bg-dark-600 text-cyan-300 px-3 py-1.5 rounded-lg border border-cyan-500/30 transition">K8s Root Pod</button>
                    <button onclick="setSample('docker')" class="text-xs bg-dark-700 hover:bg-dark-600 text-cyan-300 px-3 py-1.5 rounded-lg border border-cyan-500/30 transition">Dockerfile Únik</button>
                    <button onclick="setSample('terraform')" class="text-xs bg-dark-700 hover:bg-dark-600 text-cyan-300 px-3 py-1.5 rounded-lg border border-cyan-500/30 transition">Terraform Otevřená SG</button>
                </div>
            </div>

            <textarea id="codeSnippet" rows="8" class="w-full bg-dark-900 border border-dark-700 rounded-lg p-4 font-mono text-sm text-cyan-300 focus:outline-none focus:border-cyan-500 transition shadow-inner" placeholder="Zde vložte kód infrastruktury nebo chybový CEF/Syslog log..."></textarea>

            <div class="mt-4 flex flex-wrap items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                    <label class="text-xs text-gray-400 font-mono">Typ vstupu:</label>
                    <select id="codeType" class="bg-dark-900 border border-dark-700 rounded px-3 py-1 text-xs font-mono text-gray-300 focus:outline-none focus:border-cyan-500">
                        <option value="cef_log">CEF / Syslog záznam</option>
                        <option value="kubernetes">Kubernetes (YAML)</option>
                        <option value="dockerfile">Dockerfile</option>
                        <option value="terraform">Terraform (HCL)</option>
                    </select>
                </div>
                <button id="btnAudit" onclick="runAudit()" class="bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-dark-900 font-bold px-6 py-2.5 rounded-lg transition duration-200 shadow-lg shadow-cyan-500/20 flex items-center gap-2">
                    <span id="btnText">Analyzovat & Auditovat</span>
                    <svg id="btnSpinner" class="hidden animate-spin h-4 w-4 text-dark-900" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path></svg>
                </button>
            </div>
        </section>

        <!-- LLMOps Lišta pozorovatelnosti -->
        <div id="llmopsBar" class="bg-dark-800/90 border border-dashed border-cyan-500/30 rounded-xl px-5 py-3 flex flex-wrap items-center justify-between text-xs font-mono text-gray-300 gap-3">
            <div class="flex items-center gap-2"><span class="text-gray-500">⏱️ Latence:</span> <span id="resLatency" class="text-purple-400 font-bold">--</span></div>
            <div class="flex items-center gap-2"><span class="text-gray-500">📊 Spotřeba tokenů:</span> <span id="resTokens" class="text-cyan-400 font-bold">--</span></div>
            <div class="flex items-center gap-2"><span class="text-gray-500">💰 Cena auditu:</span> <span id="resCost" class="text-emerald-400 font-bold">--</span></div>
            <div class="flex items-center gap-2"><span class="text-gray-500">🤖 Model:</span> <span id="resModel" class="text-blue-400 font-bold">gpt-5-mini</span></div>
        </div>

        <!-- Výsledkový panel -->
        <div id="resultsArea" class="space-y-6">
            <!-- 4 souhrnné karty -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-dark-800 border border-dark-700 rounded-xl p-4">
                    <div class="text-xs font-mono text-gray-400 uppercase">Závažnost</div>
                    <div id="resSeverity" class="text-2xl font-black mt-1 text-gray-500">--</div>
                </div>
                <div class="bg-dark-800 border border-dark-700 rounded-xl p-4">
                    <div class="text-xs font-mono text-gray-400 uppercase">Compliance / Zdraví</div>
                    <div id="resScore" class="text-2xl font-black mt-1 text-gray-500">--</div>
                </div>
                <div class="bg-dark-800 border border-dark-700 rounded-xl p-4">
                    <div class="text-xs font-mono text-gray-400 uppercase">Počet rizik</div>
                    <div id="resFindingsCount" class="text-2xl font-black mt-1 text-gray-500">--</div>
                </div>
                <div class="bg-dark-800 border border-dark-700 rounded-xl p-4">
                    <div class="text-xs font-mono text-gray-400 uppercase">Bezpečnostní verdikt</div>
                    <div id="resVerdict" class="text-2xl font-black mt-1 text-gray-500">--</div>
                </div>
            </div>

            <!-- Souhrn incidentu -->
            <div class="bg-dark-800 border border-dark-700 rounded-xl p-5">
                <h3 class="text-sm font-bold text-gray-300 font-mono mb-2 uppercase tracking-wider">Souhrn auditu & SRE zpráva</h3>
                <p id="resSummary" class="text-sm text-gray-300 leading-relaxed font-sans">Čekám na odeslání vstupu k analýze...</p>
            </div>

            <!-- Detaily: Nálezy a oprava -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Bezpečnostní a provozní nálezy -->
                <div class="bg-dark-800 border border-dark-700 rounded-xl p-5 flex flex-col">
                    <h3 class="text-sm font-bold text-gray-300 font-mono mb-3 uppercase tracking-wider">Bezpečnostní & Provozní nálezy</h3>
                    <div id="resFindingsList" class="space-y-3 flex-1 overflow-y-auto max-h-[420px] pr-2">
                        <div class="text-xs text-gray-500 italic">Zatím nebyly detekovány žádné nálezy.</div>
                    </div>
                </div>

                <!-- Auto-Remediation / Runbook -->
                <div class="bg-dark-800 border border-dark-700 rounded-xl p-5 flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <h3 class="text-sm font-bold text-gray-300 font-mono uppercase tracking-wider">Auto-Remediation / Runbook</h3>
                        <button onclick="copySnippet()" class="text-xs bg-dark-700 hover:bg-dark-600 text-gray-300 px-2.5 py-1 rounded border border-dark-600 transition font-mono">Kopírovat</button>
                    </div>
                    <pre id="resSnippet" class="bg-dark-900 border border-dark-700 rounded-lg p-4 font-mono text-xs text-emerald-400 overflow-x-auto flex-1 max-h-[420px]"># Zde se vygeneruje opravený manifest nebo diagnostický postup...</pre>
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t border-dark-700 py-4 bg-dark-800/40 text-center text-xs text-gray-500 font-mono">
        CloudPulse Guard © 2026 | Vyvinuto pro NOTIX SRE & SecOps | Azure AI Foundry
    </footer>

    <script>
        const samples = {
            cef: `CEF:1|Notix|security-gateway|2.1.0|||8| rt=Nov 10 2026 14:21:11.128 UTC cs1Label=ApplicationName cs1=security-gateway cs2Label=Class.Method cs2=c.m.p.b.c.e.h.LastExceptionHandler.handleForbidden cs3Label=ExceptionType cs3=WebClientRequestException cs4Label=Thread cs4=https-jsse-nio-8443-exec-8 cs5Label=RequestUrl cs5=/auth/login cs6Label=Msg cs6=connection timed out after 30000 ms: auth.cms.gov.cz/94.199.44.157:443 flexString1Label=SID flexString1=`,
            k8s: `apiVersion: apps/v1
kind: Deployment
metadata:
  name: notix-auth-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: auth-container
        image: notix/auth:v2.1
        securityContext:
          privileged: true
          runAsUser: 0
        ports:
        - containerPort: 8080`,
            docker: `FROM python:3.11-alpine
ENV API_KEY="ghp_LiveProductionSecretKeyNotix12345678"
USER root
COPY . /app
WORKDIR /app
CMD ["python", "app.py"]`,
            terraform: `resource "aws_security_group" "public_web" {
  name        = "open-access-sg"
  description = "Public ingress rule"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}`
        };

        function setSample(type) {
            document.getElementById('codeSnippet').value = samples[type] || '';
            const typeMap = { cef: 'cef_log', k8s: 'kubernetes', docker: 'dockerfile', terraform: 'terraform' };
            document.getElementById('codeType').value = typeMap[type] || 'kubernetes';
        }

        async function runAudit() {
            const snippet = document.getElementById('codeSnippet').value.trim();
            const codeType = document.getElementById('codeType').value;
            if (!snippet) {
                alert('Vložte prosím kód nebo chybový log k analýze.');
                return;
            }

            const btnText = document.getElementById('btnText');
            const btnSpinner = document.getElementById('btnSpinner');
            btnText.innerText = 'Probíhá audit...';
            btnSpinner.classList.remove('hidden');

            try {
                const resp = await fetch('/api/audit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code_snippet: snippet, code_type: codeType })
                });

                if (!resp.ok) throw new Error('Chyba při komunikaci s API');
                const data = await resp.json();

                // LLMOps lišta
                document.getElementById('resLatency').innerText = data.latency_seconds + ' s';
                document.getElementById('resTokens').innerText = data.total_tokens + ' (vstup: ' + data.prompt_tokens + ', výstup: ' + data.completion_tokens + ')';
                document.getElementById('resCost').innerText = '$' + data.cost_usd.toFixed(6);
                document.getElementById('resModel').innerText = data.model_used;

                // Karty
                const sevElem = document.getElementById('resSeverity');
                sevElem.innerText = data.severity;
                sevElem.className = 'text-2xl font-black mt-1 ' + (data.severity === 'CRITICAL' ? 'text-rose-500' : data.severity === 'HIGH' ? 'text-amber-500' : 'text-emerald-500');

                document.getElementById('resScore').innerText = data.compliance_score + ' / 100';
                document.getElementById('resFindingsCount').innerText = data.findings.length + ' nálezů';

                const verdictElem = document.getElementById('resVerdict');
                if (data.compliance_score >= 80) {
                    verdictElem.innerText = 'SCHVÁLENO';
                    verdictElem.className = 'text-2xl font-black mt-1 text-emerald-400';
                } else {
                    verdictElem.innerText = 'SELHÁNÍ / RIZIKO';
                    verdictElem.className = 'text-2xl font-black mt-1 text-rose-500';
                }

                document.getElementById('resSummary').innerText = data.summary;

                // Seznam nálezů
                const findingsContainer = document.getElementById('resFindingsList');
                findingsContainer.innerHTML = '';
                if (data.findings.length === 0) {
                    findingsContainer.innerHTML = '<div class="text-xs text-emerald-400 font-mono">Nebyly nalezeny žádné bezpečnostní ani provozní nedostatky.</div>';
                } else {
                    data.findings.forEach(f => {
                        const item = document.createElement('div');
                        item.className = 'p-3 rounded-lg border border-dark-700 bg-dark-900/60';
                        item.innerHTML = `
                            <div class="flex items-center justify-between mb-1">
                                <span class="font-bold text-sm text-gray-200">${f.issue}</span>
                                <span class="text-[10px] font-mono px-2 py-0.5 rounded ${f.severity === 'CRITICAL' ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-amber-950 text-amber-400 border border-amber-800'}">${f.severity}</span>
                            </div>
                            <p class="text-xs text-gray-400 mt-1">${f.recommendation}</p>
                        `;
                        findingsContainer.appendChild(item);
                    });
                }

                document.getElementById('resSnippet').innerText = data.remediated_snippet || '# Žádné nápravné kroky nebyly navrženy.';

            } catch (err) {
                alert('Audit selhal: ' + err.message);
            } finally {
                btnText.innerText = 'Analyzovat & Auditovat';
                btnSpinner.classList.add('hidden');
            }
        }

        function copySnippet() {
            const snippet = document.getElementById('resSnippet').innerText;
            navigator.clipboard.writeText(snippet);
            alert('Nápravný kód / runbook byl zkopírován do schránky!');
        }
    </script>
</body>
</html>
"""
