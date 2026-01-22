from prompts import article_prompt
from generator import generate_article

response = generate_article(article_prompt, "Boosting Brand Loyalty Through Personalized Content Strategies", "marketing (Social Media Marketing, Digital Marketing, SEO etc.)")

print(response)
