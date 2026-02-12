article_prompt = """
    You are an expert {category_description} writer.
    
    Write a high-quality, original, human-like article based on the following title:
    
    Title: {title}
    
    Article Requirements:
    - Length: 700–900 words
    - Clear, professional English
    - Suitable for beginners to intermediate readers
    - Concise but insightful
    - Avoid fluff, repetition, and generic filler
    - Do NOT mention AI, prompts, or instructions
    
    phpBB Formatting Rules (STRICT):
    - Use ONLY these BBCode tags: [b] and [code]
    - Use [b] ONLY for section titles
    - Use 3–5 sections maximum
    - Each [b] section title must be on its own line
    - Leave exactly one blank line before and after each [b] section
    - Leave one blank line before and after each [code] block
    - Do NOT nest BBCode tags
    - Do NOT place [b] inside [code]
    - Do NOT place [code] inside [b]
    - Do NOT use Markdown
    - Do NOT use bullet points
    - Do NOT use numbered lists
    - Do NOT use emojis
    - Do NOT use excessive capitalization
    - Do NOT add decorative separators
    
    Content Guidelines:
    - Start with a strong opening section explaining why the topic matters in {category_description}
    - Explain core concepts clearly and efficiently
    - Include practical applications and best practices
    - If relevant, include 1–2 short [code] examples only
    - Briefly discuss common mistakes and how to avoid them
    - End with a concise, practical conclusion section
    
    SEO Guidelines:
    - Naturally include keywords related to the title and {category_description}
    - Use semantic variations
    - Avoid keyword stuffing
    - Maintain natural human tone
    
    Anti-Spam Optimization:
    - Avoid repetitive sentence patterns
    - Avoid overly promotional tone
    - Avoid exaggerated claims
    - Keep paragraph lengths varied
    - Maintain natural language flow
    
    Output Rules:
    - Return ONLY the formatted article
    - No commentary before or after
    - No extra text outside the article
"""

title_prompt = """
    You are an expert content writer and {category_description} strategist.
    
    Generate EXACTLY {batch_size} UNIQUE article titles for the category:
    "{category_description}"
    
    STRICT RULES:
    - No title may reuse phrasing, structure, or wording from another title.
    - Avoid repeating common patterns like:
      "Ultimate Guide", "How to", "Top X", "Best Practices"
    - Vary title styles:
      - Questions
      - Data-driven
      - Problem–solution
      - Beginner-focused
      - Advanced strategy
      - Trends & future
      - Case-study inspired
    - Each title must explore a DIFFERENT angle of the category.
    - Length: 6–12 words.
    - Titles must sound natural and human-written.
    
    DO NOT reuse or paraphrase any title from this list:
    {existing_titles}
    
    Output format:
    1. Title
    2. Title
    ...
    {batch_size}. Title
    
    Output ONLY the numbered titles. No explanations.

"""

