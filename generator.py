import requests
# ===============================
# CONFIGURATION
# ===============================
# Replace <MAC_IP> with your Mac mini LAN IP
OLLAMA_URL = "http://192.168.88.223:11434/api/generate"

# Available models to choose from
MODELS = [
    "qwen2.5:7b-instruct",
    "qwen3:8b",
    "llama3.1:8b"
]

# Model name is optional here, the Mac server handles it
MODEL = MODELS[0]


# ===============================
# HELPER FUNCTION
# ===============================
def generate_response(prompt, title):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt.format(title),
            "stream": False,
            "options": {"temperature": 0.7, "top_p": 0.9}
        }
    )
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return f"Error: {response.status_code} - {response.text}"