# 🆓 FREE AI-Powered SEO Auto-Tagger Setup Guide

## ✨ Using Google Gemini API (100% FREE!)

Google Gemini offers a **completely free tier** with generous limits:
- ✅ **15 requests per minute** (FREE forever)
- ✅ **No credit card required**
- ✅ **High quality AI** (Gemini 1.5 Flash)
- ✅ **Better than rule-based** analysis

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your FREE API Key

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSy...`)

That's it! No credit card, no payment info needed.

---

### Step 2: Install Dependencies

```bash
# Install required packages
pip install google-generativeai python-dotenv

# Or install everything
pip install -r requirements_ai.txt
```

---

### Step 3: Set Your API Key

**Option A: Environment Variable (Recommended)**
```bash
# On Mac/Linux
export GEMINI_API_KEY='your-api-key-here'

# On Windows
set GEMINI_API_KEY=your-api-key-here
```

**Option B: In Code**
```python
from ai_seo_auto_tagger import AISeOAutoTagger

# Pass directly
tagger = AISeOAutoTagger(api_key='your-api-key-here')
```

**Option C: .env File**
```bash
# Create .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

---

### Step 4: Run It!

```python
from ai_seo_auto_tagger import AISeOAutoTagger

# Initialize (will use AI if key is set)
tagger = AISeOAutoTagger()

# Process your blog
blog_text = """
# Your Amazing Blog Post

Your content here...
"""

tagger.process_and_save(
    blog_text=blog_text,
    output_path="my_blog_post.md",
    author="Your Name"
)
```

---

## 📊 AI vs Rule-Based Comparison

| Feature | Rule-Based (No API) | AI-Powered (FREE Gemini) |
|---------|-------------------|------------------------|
| **Cost** | $0 | $0 |
| **Setup** | None | 5 min (get API key) |
| **Keyword Quality** | Basic (frequency) | Excellent (contextual) |
| **Meta Description** | Generic | Compelling & click-worthy |
| **FAQ Generation** | Pattern matching | Smart extraction |
| **Context Understanding** | ❌ | ✅ |
| **Semantic Keywords** | Basic | Advanced |
| **Target Audience** | ❌ | ✅ |
| **Content Intent** | ❌ | ✅ |

**Recommendation:** Use AI-powered version - it's FREE and much better!

---

## 🎯 Usage Examples

### Example 1: Basic Usage

```python
from ai_seo_auto_tagger import AISeOAutoTagger

tagger = AISeOAutoTagger()

blog = """# 10 Tips for Better Sleep

Getting quality sleep is essential for health...
"""

tagger.process_and_save(blog, "sleep_tips.md")
```

**Output includes:**
- Focus keyword: "better sleep tips"
- Meta description: "Discover 10 science-backed tips to improve your sleep quality and wake up refreshed every morning."
- Target audience: "health-conscious individuals"
- Content intent: "informational"

### Example 2: Batch Processing

```python
import glob

tagger = AISeOAutoTagger()

for file in glob.glob("drafts/*.txt"):
    with open(file) as f:
        content = f.read()
    
    output = file.replace('.txt', '.md')
    tagger.process_and_save(content, output)
    
    print(f"✅ Processed: {file}")
```

### Example 3: Custom Metadata

```python
tagger.process_and_save(
    blog_text=blog,
    output_path="output.md",
    title="Custom Title Override",
    author="Jane Doe",
    category="Technology"
)
```

---

## 🔧 Troubleshooting

### "No Gemini API key found"

**Solution:** 
```bash
# Set environment variable
export GEMINI_API_KEY='your-key-here'

# Or create .env file
echo "GEMINI_API_KEY=your-key-here" > .env
```

### "google.generativeai not installed"

**Solution:**
```bash
pip install google-generativeai
```

### "API quota exceeded"

**Issue:** Free tier limits (15 requests/min)

**Solution:**
```python
import time

# Add delay between requests
for blog in blogs:
    tagger.process_and_save(blog, f"{i}.md")
    time.sleep(4)  # Wait 4 seconds between calls
```

### Fallback to Rule-Based

If AI fails, it automatically falls back:

```python
# Will use AI if available, rules if not
tagger = AISeOAutoTagger(use_ai=True)

# Force rule-based (no API needed)
tagger = AISeOAutoTagger(use_ai=False)
```

---

## 🌟 Advanced Features

### Get Detailed Metadata

```python
metadata = tagger.generate_seo_metadata(blog_text)

print(f"Focus Keyword: {metadata['focus_keyword']}")
print(f"Target Audience: {metadata['target_audience']}")
print(f"Content Intent: {metadata['content_intent']}")
print(f"Key Takeaways: {metadata['key_takeaways']}")
```

### Custom Prompts (Coming Soon)

```python
tagger = AISeOAutoTagger(
    custom_prompt="Focus on e-commerce keywords...",
    brand_voice="professional and technical"
)
```

---

## 📈 Rate Limits

### Free Tier Limits (Gemini)
- **15 requests per minute**
- **1,500 requests per day**
- **Unlimited total requests**

For most users, this is **more than enough**!

### Handling Limits

```python
import time
from ai_seo_auto_tagger import AISeOAutoTagger

tagger = AISeOAutoTagger()

blogs = [...]  # Your blog posts

for i, blog in enumerate(blogs):
    tagger.process_and_save(blog, f"post_{i}.md")
    
    # Rate limit: 15/min = 1 every 4 seconds
    if i < len(blogs) - 1:
        time.sleep(4)
```

---

## 🆚 Alternative Free APIs

### Option 2: Hugging Face (Free)

```python
# Install
pip install huggingface-hub

# Use
from huggingface_hub import InferenceClient

client = InferenceClient(token="your-hf-token")
# Integrate with your tagger
```

**Limits:** 30,000 characters/month (free)

### Option 3: Ollama (Local, Free)

```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download model
ollama pull llama2

# Use locally (no API key needed!)
```

**Pros:** 
- 100% free
- No API key
- Works offline

**Cons:**
- Requires local installation
- Slower than cloud APIs

---

## 💡 Pro Tips

1. **Save your API key** in `.env` file (never commit to git!)
2. **Add rate limiting** for batch processing
3. **Check generated metadata** - AI is smart but not perfect
4. **Use meaningful filenames** for easy organization
5. **Batch process at night** to avoid hitting rate limits

---

## ✅ You're Ready!

Your AI-powered SEO auto-tagger is now set up with **100% free AI**!

**Next Steps:**
1. Get your free Gemini API key
2. Set the environment variable
3. Run `python ai_seo_auto_tagger.py`
4. Start optimizing your content! 🚀

---

## 📞 Need Help?

- **API Key Issues:** https://makersuite.google.com/app/apikey
- **Gemini Docs:** https://ai.google.dev/tutorials/python_quickstart
- **Rate Limits:** Check your usage at Google AI Studio

---

**Happy tagging! 🎉**