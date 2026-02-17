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

# ✅ ADDED: Flask imports
from flask import Flask, render_template, request, jsonify

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: google-generativeai not installed. Install with: pip install google-generativeai")

# ✅ ADDED: Flask app instance (Gunicorn needs this)
app = Flask(__name__)

class AISeOAutoTagger:
    """
    AI-powered SEO auto-tagger using Google Gemini API (FREE)
    """
    
    def __init__(self, api_key: Optional[str] = None, use_ai: bool = True):
        """
        Initialize the AI-powered SEO tagger.
        
        Args:
            api_key: Google Gemini API key (get free at https://makersuite.google.com/app/apikey)
                    If None, will try to read from GEMINI_API_KEY environment variable
            use_ai: If False, falls back to rule-based approach (no API needed)
        """
        self.use_ai = use_ai and GEMINI_AVAILABLE
        
        if self.use_ai:
            # Get API key from parameter or environment
            self.api_key = api_key or os.getenv('GEMINI_API_KEY')
            
            if not self.api_key:
                print("⚠️  No Gemini API key found. Get one FREE at: https://makersuite.google.com/app/apikey")
                print("Set it with: export GEMINI_API_KEY='your-key-here'")
                print("Falling back to rule-based approach...")
                self.use_ai = False
            else:
                # Configure Gemini
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                print("✅ AI-powered mode enabled (using Google Gemini - FREE)")
        else:
            print("📝 Using rule-based approach (no AI API needed)")
    
    def ai_analyze_content(self, blog_text: str, title: Optional[str] = None) -> Dict:
        """
        Use Google Gemini AI to analyze content and generate SEO metadata.
        This is FREE - no cost!
        """
        
        prompt = f"""You are an expert SEO specialist. Analyze this blog content and generate comprehensive SEO metadata.

Blog Content:
{blog_text}

Generate a JSON response with the following fields:

1. **focus_keyword**: The single most important keyword (2-4 words)
2. **keywords**: Array of 10-12 primary keywords and phrases
3. **semantic_keywords**: Array of 5-8 LSI/related keyword phrases
4. **meta_description**: Compelling, action-oriented meta description (150-155 characters)
5. **meta_title**: SEO-optimized title (55-60 characters, include focus keyword)
6. **tags**: 8-10 content tags (capitalize first letter)
7. **category**: Best fitting category (Technology/Business/Health/Lifestyle/Education/etc)
8. **entities**: Named entities - people, places, organizations mentioned
9. **topics**: Main topics/themes covered (from headings)
10. **faq_questions**: Array of 3-5 FAQ items with "question" and "answer" (extract from content or generate)
11. **target_audience**: Who this content is for (e.g., "developers", "marketers", "healthcare professionals")
12. **content_intent**: One of: informational, commercial, navigational, transactional
13. **readability_level**: Estimated grade level (e.g., "high school", "college", "professional")
14. **key_takeaways**: 3-5 bullet points of main insights

IMPORTANT: 
- Return ONLY valid JSON, no markdown formatting, no backticks
- Make meta_description compelling and click-worthy
- Ensure meta_title includes the focus keyword
- Keywords should be actual phrases from the content
- FAQ answers should be 1-2 sentences

Return the JSON now:"""

        try:
            # Call Gemini API (FREE!)
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            json_text = response.text.strip()
            
            # Remove markdown formatting if present
            json_text = re.sub(r'^```json\s*', '', json_text)
            json_text = re.sub(r'\s*```$', '', json_text)
            
            metadata = json.loads(json_text)
            
            return metadata
            
        except Exception as e:
            print(f"⚠️  AI analysis failed: {e}")
            print("Falling back to rule-based approach...")
            return None
    
    def rule_based_analysis(self, blog_text: str, title: Optional[str] = None) -> Dict:
        """
        Fallback rule-based analysis (no AI needed)
        """
        # Extract title
        lines = blog_text.strip().split('\n')
        if not title:
            title = re.sub(r'^#+\s*', '', lines[0]).strip() if lines else "Untitled"
        
        # Simple keyword extraction
        words = re.findall(r'\b[a-z]{3,}\b', blog_text.lower())
        stop_words = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'will'}
        
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords = [word for word, _ in top_words]
        
        # Generate meta description
        sentences = re.split(r'[.!?]+', re.sub(r'^#+.*$', '', blog_text, flags=re.MULTILINE))
        clean_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        meta_desc = '. '.join(clean_sentences[:2])[:155]
        
        # Extract topics from headings
        topics = re.findall(r'^#{1,3}\s+(.+)$', blog_text, re.MULTILINE)
        
        return {
            'focus_keyword': keywords[0] if keywords else 'content',
            'keywords': keywords[:10],
            'semantic_keywords': [f"{keywords[i]} {keywords[i+1]}" for i in range(min(5, len(keywords)-1))],
            'meta_description': meta_desc or blog_text[:155],
            'meta_title': title[:60],
            'tags': [k.capitalize() for k in keywords[:8]],
            'category': 'General',
            'entities': [],
            'topics': topics[:5],
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
        """
        Generate comprehensive SEO metadata using AI or rule-based approach.
        """
        
        # Try AI first if enabled
        if self.use_ai:
            ai_metadata = self.ai_analyze_content(blog_text, title)
            if ai_metadata:
                # Use AI metadata
                base_metadata = ai_metadata
            else:
                # AI failed, use rules
                base_metadata = self.rule_based_analysis(blog_text, title)
        else:
            # Use rule-based
            base_metadata = self.rule_based_analysis(blog_text, title)
        
        # Override with user-provided values
        if title:
            base_metadata['meta_title'] = title[:60]
        if author:
            base_metadata['author'] = author
        if category:
            base_metadata['category'] = category
        
        # Add technical metadata
        today = datetime.now().strftime('%Y-%m-%d')
        word_count = len(blog_text.split())
        reading_time = max(1, round(word_count / 200))
        
        # Generate slug from title
        slug_title = base_metadata.get('meta_title', 'untitled')
        slug = re.sub(r'[^\w\s-]', '', slug_title.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')[:60]
        
        # Complete metadata
        complete_metadata = {
            'title': base_metadata.get('meta_title', 'Untitled'),
            'meta_title': base_metadata.get('meta_title', 'Untitled'),
            'meta_description': base_metadata.get('meta_description', ''),
            'author': base_metadata.get('author', 'Content Team'),
            'date': today,
            'category': base_metadata.get('category', 'General'),
            'slug': slug,
            'canonical_url': f"/{slug}",
            'robots': 'index, follow',
            
            # SEO
            'focus_keyword': base_metadata.get('focus_keyword', ''),
            'keywords': base_metadata.get('keywords', []),
            'tags': base_metadata.get('tags', []),
            'semantic_keywords': base_metadata.get('semantic_keywords', []),
            
            # Social
            'og_title': base_metadata.get('meta_title', ''),
            'og_description': base_metadata.get('meta_description', '')[:200],
            'og_type': 'article',
            'twitter_card': 'summary_large_image',
            
            # AEO
            'schema_type': 'BlogPosting',
            'reading_time': f"{reading_time} min read",
            'word_count': word_count,
            'faq_schema': base_metadata.get('faq_questions', []),
            
            # Advanced
            'entities': base_metadata.get('entities', []),
            'topics': base_metadata.get('topics', []),
            'target_audience': base_metadata.get('target_audience', ''),
            'content_intent': base_metadata.get('content_intent', 'informational'),
            'readability_level': base_metadata.get('readability_level', ''),
            'key_takeaways': base_metadata.get('key_takeaways', []),
        }
        
        return complete_metadata
    
    def create_markdown_file(self, blog_text: str, 
                            metadata: Optional[Dict] = None,
                            **kwargs) -> str:
        """
        Create markdown file with YAML frontmatter.
        """
        
        if metadata is None:
            metadata = self.generate_seo_metadata(blog_text, **kwargs)
        
        # Build YAML frontmatter
        yaml_lines = ['---']
        
        # Basic
        yaml_lines.append(f'title: "{metadata["title"]}"')
        yaml_lines.append(f'meta_title: "{metadata["meta_title"]}"')
        yaml_lines.append(f'description: "{metadata["meta_description"]}"')
        yaml_lines.append(f'date: {metadata["date"]}')
        yaml_lines.append(f'author: {metadata["author"]}')
        yaml_lines.append(f'category: {metadata["category"]}')
        yaml_lines.append(f'slug: {metadata["slug"]}')
        yaml_lines.append(f'canonical: {metadata["canonical_url"]}')
        yaml_lines.append(f'robots: {metadata["robots"]}')
        yaml_lines.append('')
        
        # SEO
        yaml_lines.append('# SEO Metadata')
        yaml_lines.append(f'focus_keyword: "{metadata["focus_keyword"]}"')
        yaml_lines.append('keywords:')
        for kw in metadata['keywords'][:10]:
            yaml_lines.append(f'  - {kw}')
        yaml_lines.append('')
        
        # Tags
        yaml_lines.append('tags:')
        for tag in metadata['tags'][:10]:
            yaml_lines.append(f'  - {tag}')
        yaml_lines.append('')
        
        # Semantic
        if metadata.get('semantic_keywords'):
            yaml_lines.append('semantic_keywords:')
            for sk in metadata['semantic_keywords'][:8]:
                yaml_lines.append(f'  - "{sk}"')
            yaml_lines.append('')
        
        # Social
        yaml_lines.append('# Social Media')
        yaml_lines.append(f'og_title: "{metadata["og_title"]}"')
        yaml_lines.append(f'og_description: "{metadata["og_description"]}"')
        yaml_lines.append(f'og_type: {metadata["og_type"]}')
        yaml_lines.append(f'twitter_card: {metadata["twitter_card"]}')
        yaml_lines.append('')
        
        # AEO
        yaml_lines.append('# Answer Engine Optimization')
        yaml_lines.append(f'schema_type: {metadata["schema_type"]}')
        yaml_lines.append(f'reading_time: {metadata["reading_time"]}')
        yaml_lines.append(f'word_count: {metadata["word_count"]}')
        
        if metadata.get('target_audience'):
            yaml_lines.append(f'target_audience: {metadata["target_audience"]}')
        if metadata.get('content_intent'):
            yaml_lines.append(f'content_intent: {metadata["content_intent"]}')
        if metadata.get('readability_level'):
            yaml_lines.append(f'readability_level: {metadata["readability_level"]}')
        yaml_lines.append('')
        
        # Topics
        if metadata.get('topics'):
            yaml_lines.append('topics:')
            for topic in metadata['topics']:
                yaml_lines.append(f'  - "{topic}"')
            yaml_lines.append('')
        
        # Entities
        if metadata.get('entities'):
            yaml_lines.append('entities:')
            for entity in metadata['entities'][:10]:
                yaml_lines.append(f'  - {entity}')
            yaml_lines.append('')
        
        # Key Takeaways
        if metadata.get('key_takeaways'):
            yaml_lines.append('key_takeaways:')
            for takeaway in metadata['key_takeaways']:
                yaml_lines.append(f'  - "{takeaway}"')
            yaml_lines.append('')
        
        # FAQ Schema
        if metadata.get('faq_schema'):
            yaml_lines.append('faq_schema:')
            for faq in metadata['faq_schema'][:5]:
                yaml_lines.append(f'  - question: "{faq.get("question", "")}"')
                yaml_lines.append(f'    answer: "{faq.get("answer", "")}"')
            yaml_lines.append('')
        
        yaml_lines.append('---')
        
        # Combine with original content
        frontmatter = '\n'.join(yaml_lines)
        markdown_content = f"{frontmatter}\n\n{blog_text}"
        
        return markdown_content
    
    def process_and_save(self, blog_text: str, output_path: str, **kwargs):
        """
        Process blog text and save to markdown file.
        """
        markdown_content = self.create_markdown_file(blog_text, **kwargs)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ SEO-optimized markdown saved: {output_path}")
        return output_path



# ----------------------------
# ✅ ADDED: FLASK ROUTES
# ----------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    blog_text = data.get("blog_text")

    if not blog_text:
        return jsonify({"error": "No blog text provided"}), 400

    try:
        tagger = AISeOAutoTagger()  # create inside request
        metadata = tagger.ai_analyze_content(blog_text)

        if not metadata:
            return jsonify({"error": "AI failed"}), 500

        return jsonify(metadata)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ----------------------------
# ✅ MODIFIED: Run Flask if local
# ----------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)