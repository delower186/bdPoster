from prompts import title_prompt
from generator import generate_titles

response = generate_titles(title_prompt, 500, "marketing (Social Media Marketing, Digital Marketing, SEO etc.)")

print(response)
