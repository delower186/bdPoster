article_prompt = """
    You are an expert { category_description } writer.
    
    Write a high-quality, original, human-like article based on the following title:
    
    Title: {{title}}
    
    Article requirements:
    - Length: 900–1200 words
    - Write in clear, professional English
    - Suitable for beginners to intermediate developers
    - Avoid fluff, repetition, and generic explanations
    - Do NOT mention AI, prompts, or instructions
    
    Structure:
    1. Introduction
       - Briefly explain what the topic is
       - Explain why it is important
    
    2. Main Content
       - Use clear section titles written as plain text
       - Explain concepts step by step
       - Include practical examples and best practices
       - For Web Development topics:
         - Explain HTML, CSS, JavaScript, backend, or performance concepts where relevant
       - For Android Development topics:
         - Explain Kotlin or Java concepts where relevant
         - Discuss Android components, architecture, and performance
    
    3. Examples
       - Include code examples written as plain text
       - Keep code simple and readable
    
    4. Common Mistakes or Pitfalls
       - List common errors developers make
       - Explain how to avoid them
    
    5. FAQ Section
       - Include 3–5 common questions with clear answers
    
    6. Conclusion
       - Summarize key points
       - Give practical takeaways
       
    Use BBCode tags only:
    [b] for section titles
    [code] for code examples
    [list] and [*] for lists
    Do not use Markdown.
    
    SEO guidelines:
    - Naturally include keywords related to the title
    - Write for humans first, search engines second
    - Do not keyword stuff
    
    Output rules:
    - Plain text only
    - No Markdown
    - No special formatting
    - No emojis
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

