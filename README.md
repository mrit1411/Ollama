# Ollama

Absolutely! Here is a **professional, comprehensive, and modern `README.md`** for your project, covering all components and real-world usage, based on your screenshots and files.

---

# Ollama Kubernetes LLM Cluster with Monitoring, Autoscaling, Chaos, and Load Testing

> **Production-grade, open-source cluster for serving Ollama LLM (e.g. Gemma 2b) with full observability, autoscaling, chaos engineering, and load-testing support.**

---

## \:rocket: **Features**

* **Kubernetes Deployment** of Ollama LLM (multi-container with Prometheus metrics exporter)
* **Prometheus & Grafana** monitoring stack (dashboards, ServiceMonitor, alert rules)
* **Horizontal Pod Autoscaler** based on custom latency metric
* **Real-world Load Testing** with Locust (Python) & K6 (JS)
* **Chaos Engineering** (manual & Chaos Mesh ready)
* **Ngrok** support for secure public API/UI tunneling
* **Easy setup:** Docker, YAML, and one-liners

---

## \:open\_file\_folder: **Repository Structure**

```
.
├── Dockerfile                 # Ollama container (Gemma, entrypoint)
├── Dockerfile.exporter        # Prometheus exporter (Flask)
├── entrypoint.sh              # Ollama startup script
├── locustfile.py              # Locust load testing
├── metrics_exporter.py        # Custom Prometheus exporter
├── ollama-deployment.yaml     # Kubernetes deployment (multi-container)
├── ollama-hpa.yaml            # HPA autoscaling config
├── ollama-alerts.yaml         # Prometheus alert rules
├── ollama-servicemonitor.yaml # ServiceMonitor for Prometheus
├── prom-stack-prometheus-svc.yaml # Prometheus service
├── prometheus-adapter-values.yaml # Prometheus adapter values
├── start-ollama-ngrok.sh      # Ngrok helper script
├── README.md                  # This file
└── ... (other helper/demo files)
```

---

## \:whale: **1. Build Docker Images**

### Ollama (main container):

```bash
docker build -t ollama-gemma:latest -f Dockerfile .
```

### Prometheus Exporter (sidecar):

```bash
docker build -t ollama-exporter:latest -f Dockerfile.exporter .
```

Push these to your registry (optional for local/Minikube testing).

---

## \:cloud: **2. Deploy to Kubernetes**

### 2.1 Deploy Ollama + Exporter

```bash
kubectl apply -f ollama-deployment.yaml
```

### 2.2 Expose Ollama (if needed)

Update/create a Service to expose Ollama or use port-forward:

```bash
kubectl port-forward deployment/ollama 11434:11434
kubectl port-forward deployment/ollama 8000:8000 # for metrics exporter
```

---

## \:chart\_with\_upwards\_trend: **3. Monitoring Setup**

### 3.1 Deploy Prometheus, Grafana (Helm recommended)

<details>
<summary>Install with Helm (if not already installed):</summary>

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install prom-stack prometheus-community/kube-prometheus-stack
```

</details>

### 3.2 Register Ollama Metrics with Prometheus

```bash
kubectl apply -f ollama-servicemonitor.yaml
```

### 3.3 Load Custom Alert Rules

```bash
kubectl apply -f ollama-alerts.yaml
```

---

## \:bar\_chart: **4. Horizontal Pod Autoscaler (HPA)**

* Scales pods based on custom metric: `ollama_avg_delay_seconds`
* Example in `ollama-hpa.yaml`:

```bash
kubectl apply -f ollama-hpa.yaml
```

---

## \:bell: **5. Alerts and Notifications**

* PrometheusRule: `ollama-alerts.yaml` (latency, timeouts)

* Configure **Grafana SMTP** for email alerts:

  * Edit `grafana.ini` or Helm values, e.g.:

    ```ini
    [smtp]
    enabled = true
    host = smtp.gmail.com:587
    user = <your-gmail>
    password = <your-app-password>
    from_address = <your-gmail>
    from_name = Grafana
    skip_verify = false
    ```

  * Restart Grafana pod after changes.

* **Set your contact points** in Grafana UI under Alerting → Contact Points.

---

## \:hammer: **6. Load Testing**

### 6.1 Locust (Python, UI-based)

```bash
# From your repo directory:
locust -f locustfile.py --host http://localhost:11434
# or use your Ngrok/Gateway endpoint
```

* Web UI at `http://localhost:8089`
* Script customizable in `locustfile.py`

### 6.2 K6 (Optional, CLI/CI friendly)

```bash
# Install k6: https://k6.io/docs/getting-started/installation/
k6 run --vus 10 --duration 30s script.js
```

* Example script included.

---

## \:test\_tube: **7. Chaos Testing**

### 7.1 Manual Pod Deletion (simple chaos)

```bash
kubectl get pods -l app=ollama -o name | shuf -n 1 | xargs kubectl delete
```

### 7.2 Chaos Mesh (for advanced chaos)

* [Install Chaos Mesh](https://chaos-mesh.org/docs/quick-start/)
* Example `podchaos.yaml`:

  ```yaml
  apiVersion: chaos-mesh.org/v1alpha1
  kind: PodChaos
  metadata:
    name: kill-ollama
  spec:
    action: pod-kill
    mode: one
    selector:
      namespaces: [default]
      labelSelectors:
        "app": "ollama"
    duration: "30s"
    scheduler:
      cron: "@every 5m"
  ```
* Apply with:

  ```bash
  kubectl apply -f podchaos.yaml
  ```

---

## \:satellite: **8. Secure Public Access with Ngrok**

Expose Locust, Grafana, or Ollama endpoints for remote testing:

```bash
ngrok http 8089   # Expose Locust UI
ngrok http 11434  # Expose Ollama API
```

---

## \:mag: **9. Troubleshooting & Tips**

* **Metrics not scraping?** Check ServiceMonitor labels, Prometheus targets, and exporter logs.
* **Email alerts not working?** Double-check SMTP config and logs in Grafana pod.
* **Auto-scaling not working?** Verify metric is exposed and Prometheus Adapter is configured.
* **Grafana dashboards missing?** Import JSON dashboard or use premade panels.
* **Pod fails?** Check `kubectl logs` for detailed errors.

---

## \:handshake: **Contributing**

PRs and issues welcome! Please open an issue for questions, improvements, or bugs.

---

## \:page\_facing\_up: **References**

* [Ollama LLM](https://ollama.com/)
* [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator)
* [Grafana](https://grafana.com/)
* [Locust](https://locust.io/)
* [K6](https://k6.io/)
* [Chaos Mesh](https://chaos-mesh.org/)

---

## \:sparkles: **Maintainers**

* **Mrityunjay Singh**
  (Repo: [mrit1411/Ollama](https://github.com/mrit1411/Ollama))

---

# \:white\_check\_mark: **Quickstart**

```bash
# Build Docker images (main & exporter)
docker build -t ollama-gemma:latest -f Dockerfile .
docker build -t ollama-exporter:latest -f Dockerfile.exporter .

# Deploy to Kubernetes
kubectl apply -f ollama-deployment.yaml
kubectl apply -f ollama-hpa.yaml
kubectl apply -f ollama-servicemonitor.yaml
kubectl apply -f ollama-alerts.yaml

# Port-forward for local testing
kubectl port-forward deployment/ollama 11434:11434
kubectl port-forward deployment/ollama 8000:8000

# Load test with Locust (see http://localhost:8089)
locust -f locustfile.py --host http://localhost:11434

# Expose endpoints for remote use
ngrok http 11434
ngrok http 8089

# Check Grafana (find node port/ingress)
kubectl get svc -n <grafana-namespace>
```

---

> **Have questions or want custom integrations?** Open an issue or discussion!

---

Let me know if you want a **shorter version**, **add diagrams**, or any other section added!
