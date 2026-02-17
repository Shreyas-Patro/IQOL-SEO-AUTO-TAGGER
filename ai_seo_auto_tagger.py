#!/usr/bin/env python3
"""
AI-Powered SEO Auto-Tagging Tool using Google Gemini (FREE teir)
Takes blog text and generates SEO-optimized .md file with AI-generated metadata
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template  # ✅ ADDED

# Load environment variables
load_dotenv()

# ✅ ADDED
app = Flask(__name__)

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
                print("⚠️ No Gemini API key found. Falling back to rule-based approach...")
                self.use_ai = False
            else:
                try:
                    self.client = genai.Client(
                        api_key=self.api_key,
                        http_options={'api_version': 'v1'}
                    )
                    print("AI-powered mode enabled")
                except Exception as e:
                    print(f"Gemini init failed: {e}")
                    self.use_ai = False
        else:
            print("Using rule-based approach")

    def ai_analyze_content(self, blog_text: str, title: Optional[str] = None) -> Dict:

        prompt = f"""
You are an expert SEO specialist. Analyze this blog content and generate comprehensive SEO metadata.

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
            print(f"AI failed: {e}")
            return None

    def rule_based_analysis(self, blog_text: str, title: Optional[str] = None) -> Dict:

        lines = blog_text.strip().split('\n')
        if not title:
            title = re.sub(r'^#+\s*', '', lines[0]).strip() if lines else "Untitled"

        words = re.findall(r'\b[a-z]{3,}\b', blog_text.lower())
        stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'will'}

        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords = [word for word, _ in top_words]

        sentences = re.split(r'[.!?]+', re.sub(r'^#+.*$', '', blog_text, flags=re.MULTILINE))
        clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        meta_desc = '. '.join(clean_sentences[:2])[:155]

        topics = re.findall(r'^#{1,3}\s+(.+)$', blog_text, re.MULTILINE)

        return {
            'focus_keyword': keywords[0] if keywords else 'content',
            'keywords': keywords[:10],
            'semantic_keywords': [],
            'meta_description': meta_desc or blog_text[:155],
            'meta_title': title[:60],
            'tags': [k.capitalize() for k in keywords[:8]],
            'category': 'General',
            'entities': [],
            'topics': topics[:5],
            'faq_questions': [],
            'target_audience': 'general readers',
            'content_intent': 'informational',
            'key_takeaways': []
        }

    def generate_seo_metadata(self, blog_text: str,
                              title: Optional[str] = None,
                              author: Optional[str] = None,
                              category: Optional[str] = None) -> Dict:

        if self.use_ai:
            base_metadata = self.ai_analyze_content(blog_text, title)
            if not base_metadata:
                base_metadata = self.rule_based_analysis(blog_text, title)
        else:
            base_metadata = self.rule_based_analysis(blog_text, title)

        today = datetime.now().strftime('%Y-%m-%d')
        word_count = len(blog_text.split())
        reading_time = max(1, round(word_count / 200))

        slug = re.sub(r'[^\w\s-]', '', base_metadata['meta_title'].lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')[:60]

        return {
            'title': base_metadata.get('meta_title', 'Untitled'),
            'meta_title': base_metadata.get('meta_title', 'Untitled'),
            'meta_description': base_metadata.get('meta_description', ''),
            'author': author or 'Content Team',
            'date': today,
            'category': category or base_metadata.get('category', 'General'),
            'slug': slug,
            'reading_time': f"{reading_time} min read",
            'word_count': word_count,
            'keywords': base_metadata.get('keywords', []),
            'focus_keyword': base_metadata.get('focus_keyword', '')
        }


# ✅ ROUTE: Homepage
@app.route("/")
def home():
    return render_template("index.html")


# ✅ ROUTE: API
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data or "content" not in data:
        return jsonify({"error": "No content provided"}), 400

    blog_text = data["content"]
    author = data.get("author")
    category = data.get("category")

    tagger = AISeOAutoTagger()
    metadata = tagger.generate_seo_metadata(
        blog_text=blog_text,
        author=author,
        category=category
    )

    return jsonify(metadata)


# ✅ REQUIRED FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
