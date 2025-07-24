from locust import HttpUser, task, between
import json

class OllamaUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def generate_text(self):
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "gemma:2b",
            "prompt": "Tell me a joke about AI",
            "stream": False
        }
        self.client.post("/api/generate", headers=headers, data=json.dumps(payload))
