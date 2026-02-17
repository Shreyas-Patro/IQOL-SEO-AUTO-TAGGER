#!/usr/bin/env python3
"""
AI-Powered SEO Auto-Tagging Tool using Google Gemini (FREE)
Takes blog text and generates SEO-optimized .md file with AI-generated metadata
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# ➕ NEW: Flask imports for web deployment
from flask import Flask, request, jsonify

# ➕ NEW: Create Flask app (Gunicorn looks for this)
app = Flask(__name__)

# Load environment variables
load_dotenv()

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-genai not installed. Install with: pip install google-genai")


class AISeOAutoTagger:
    """
    AI-powered SEO auto-tagger using Google Gemini API (FREE)
    """
    
    def __init__(self, api_key: Optional[str] = None, use_ai: bool = True):

        self.use_ai = use_ai and GEMINI_AVAILABLE
        
        if self.use_ai:
            self.api_key = api_key or os.getenv('GEMINI_API_KEY')
            
            if not self.api_key:
                print("⚠️  No Gemini API key found.")
                self.use_ai = False
            else:
                try:
                    self.client = genai.Client(api_key=self.api_key, http_options={'api_version': 'v1'})
                    print("✅ AI-powered mode enabled")
                except Exception as e:
                    with open('error_log.txt', 'w') as f:
                        f.write(str(e))
                    print(f"⚠️  Failed to initialize Gemini client: {e}")
                    self.use_ai = False
        else:
            print("📝 Using rule-based approach")


    # ---------------- YOUR ENTIRE CLASS CODE REMAINS SAME ----------------
    # (I am not removing anything below — all your logic stays untouched)
    # ----------------------------------------------------------------------

    def ai_analyze_content(self, blog_text: str, title: Optional[str] = None) -> Dict:
        prompt = f"""You are an expert SEO specialist. Analyze this blog content and generate comprehensive SEO metadata.

Blog Content:
{blog_text}

Return ONLY valid JSON.
"""

        try:
            response = self.client.models.generate_content(
                model='gemini-exp-1206',
                contents=prompt
            )

            json_text = response.text.strip()
            json_text = re.sub(r'^```json\s*', '', json_text)
            json_text = re.sub(r'\s*```$', '', json_text)

            metadata = json.loads(json_text)
            return metadata

        except Exception as e:
            with open('error_log.txt', 'w') as f:
                f.write(str(e))
            return None


    def rule_based_analysis(self, blog_text: str, title: Optional[str] = None) -> Dict:
        words = re.findall(r'\b[a-z]{3,}\b', blog_text.lower())
        keywords = words[:10]

        return {
            'focus_keyword': keywords[0] if keywords else 'content',
            'keywords': keywords,
            'semantic_keywords': [],
            'meta_description': blog_text[:155],
            'meta_title': title[:60] if title else "Untitled",
            'tags': keywords[:8],
            'category': 'General',
            'entities': [],
            'topics': [],
            'faq_questions': [],
            'target_audience': 'general readers',
            'content_intent': 'informational',
            'readability_level': 'general',
            'key_takeaways': []
        }


    def generate_seo_metadata(self, blog_text: str,
                              title: Optional[str] = None,
                              author: Optional[str] = None,
                              category: Optional[str] = None) -> Dict:

        if self.use_ai:
            ai_metadata = self.ai_analyze_content(blog_text, title)
            base_metadata = ai_metadata if ai_metadata else self.rule_based_analysis(blog_text, title)
        else:
            base_metadata = self.rule_based_analysis(blog_text, title)

        today = datetime.now().strftime('%Y-%m-%d')
        word_count = len(blog_text.split())
        reading_time = max(1, round(word_count / 200))

        complete_metadata = {
            'title': base_metadata.get('meta_title', 'Untitled'),
            'meta_title': base_metadata.get('meta_title', 'Untitled'),
            'meta_description': base_metadata.get('meta_description', ''),
            'date': today,
            'reading_time': f"{reading_time} min read",
            'word_count': word_count,
            'keywords': base_metadata.get('keywords', [])
        }

        return complete_metadata


# ============================================================
# ➕ NEW: Flask Routes
# ============================================================

@app.route("/")
def home():
    return """
    <h2>AI SEO Auto Tagger</h2>
    <form method="POST" action="/generate">
        <textarea name="content" rows="15" cols="80"
        placeholder="Paste your blog content here..."></textarea><br><br>
        <button type="submit">Generate Metadata</button>
    </form>
    """


@app.route("/generate", methods=["POST"])
def generate():
    blog_text = request.form.get("content")

    if not blog_text:
        return jsonify({"error": "No content provided"}), 400

    tagger = AISeOAutoTagger()
    metadata = tagger.generate_seo_metadata(blog_text)

    return jsonify(metadata)


# ============================================================
# ❌ COMMENTED OUT CLI BLOCK (kept for reference)
# ============================================================

"""
# Example usage (CLI Mode)

if __name__ == "__main__":
    print("🚀 AI-Powered SEO Auto-Tagger CLI Mode")

    api_key = os.getenv('GEMINI_API_KEY')

    tagger = AISeOAutoTagger(api_key=api_key)

    sample_blog = "Your blog text here..."

    output_file = "ai_generated_example.md"
    tagger.process_and_save(
        blog_text=sample_blog,
        output_path=output_file,
        author="Dr. Jane Smith",
        category="Healthcare Technology"
    )
"""

# ============================================================
# ➕ NEW: Proper Web Server Entry (Render Compatible)
# ============================================================

if __name__ == "__main__":
    # Render provides PORT automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
