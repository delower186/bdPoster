import requests

from browser.utilities import remove_non_bmp

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
def generate_article(prompt, title, category_description):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt.format(title=title, category_description=category_description),
            "stream": False,
            "options": {"temperature": 0.7, "top_p": 0.9}
        }
    )
    if response.status_code == 200:
        response_content = response.json().get("response", "").replace("***", "").replace("**", "").replace("##", "").replace("#", "")
        cleaned_content = remove_non_bmp(response_content)

        return cleaned_content

    else:
        return f"Error: {response.status_code} - {response.text}"


def generate_titles(prompt, category_description, batch_size, all_titles):
    existing_titles = "\n".join(list(all_titles)[-100:])

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt.format(
                category_description=category_description,
                batch_size=batch_size,
                existing_titles=existing_titles
            ),
            "stream": False,
            "options": {
                "temperature": 0.9,
                "top_p": 0.95,
                "max_tokens": 800
            }
        }
    )

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    title_response = response.json().get("response", "")

    parsed_titles = [
        line.split(". ", 1)[-1].strip()
        for line in title_response.splitlines()
        if line.strip() and line[0].isdigit()
    ]

    # Keep ONLY truly new titles
    new_only = set()

    for title in parsed_titles:
        if title not in all_titles:
            all_titles.add(title)
            new_only.add(title)

    return new_only


