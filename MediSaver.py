#!/usr/bin/env python3
"""
Medicine Alternatives Finder
------------------------------
Requirements: pip install flask requests
Run:          python medicine_finder.py
Then open:    http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# ---------------------------------------------------------------------------
# HTML / CSS / JS (all embedded in one file)
# ---------------------------------------------------------------------------

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Medicine Alternatives Finder</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      min-height: 100vh;
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      font-family: 'Segoe UI', system-ui, sans-serif;
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 16px 60px;
    }

    .header {
      text-align: center;
      margin-bottom: 36px;
    }
    .header h1 {
      font-size: 2.2rem;
      font-weight: 700;
      letter-spacing: -0.5px;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .header p {
      margin-top: 8px;
      color: #94a3b8;
      font-size: 0.95rem;
    }

    .card {
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 32px;
      width: 100%;
      max-width: 680px;
    }

    .form-group {
      margin-bottom: 20px;
    }
    label {
      display: block;
      font-size: 0.82rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: #94a3b8;
      margin-bottom: 8px;
    }
    input[type="text"], input[type="password"] {
      width: 100%;
      padding: 12px 16px;
      background: rgba(255,255,255,0.07);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 10px;
      color: #e2e8f0;
      font-size: 1rem;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    input:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 3px rgba(56,189,248,0.15);
    }
    input::placeholder { color: #475569; }

    .key-row {
      display: flex;
      gap: 10px;
      align-items: flex-end;
    }
    .key-row .form-group { flex: 1; margin-bottom: 0; }
    .toggle-btn {
      padding: 12px 14px;
      background: rgba(255,255,255,0.07);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 10px;
      color: #94a3b8;
      cursor: pointer;
      font-size: 1rem;
      transition: background 0.2s;
      white-space: nowrap;
    }
    .toggle-btn:hover { background: rgba(255,255,255,0.13); }

    .search-btn {
      width: 100%;
      padding: 14px;
      margin-top: 8px;
      background: linear-gradient(135deg, #38bdf8, #818cf8);
      border: none;
      border-radius: 10px;
      color: #0f172a;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      transition: opacity 0.2s, transform 0.1s;
      letter-spacing: 0.02em;
    }
    .search-btn:hover { opacity: 0.92; }
    .search-btn:active { transform: scale(0.99); }
    .search-btn:disabled { opacity: 0.5; cursor: not-allowed; }

    .spinner {
      display: none;
      text-align: center;
      padding: 30px 0 10px;
    }
    .spinner-ring {
      display: inline-block;
      width: 40px; height: 40px;
      border: 3px solid rgba(56,189,248,0.2);
      border-top-color: #38bdf8;
      border-radius: 50%;
      animation: spin 0.75s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    .error-box {
      display: none;
      margin-top: 24px;
      padding: 14px 18px;
      background: rgba(239,68,68,0.12);
      border: 1px solid rgba(239,68,68,0.35);
      border-radius: 10px;
      color: #fca5a5;
      font-size: 0.9rem;
    }

    .results { margin-top: 32px; }

    .section-title {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #64748b;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .section-title::after {
      content: '';
      flex: 1;
      height: 1px;
      background: rgba(255,255,255,0.08);
    }

    .alt-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 10px;
      margin-bottom: 32px;
    }
    .alt-pill {
      background: rgba(56,189,248,0.1);
      border: 1px solid rgba(56,189,248,0.25);
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 0.88rem;
      font-weight: 500;
      color: #7dd3fc;
      word-break: break-word;
    }

    .result-list { list-style: none; }
    .result-item {
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 14px 16px;
      margin-bottom: 10px;
      transition: background 0.2s;
    }
    .result-item:hover { background: rgba(255,255,255,0.08); }
    .result-item .title {
      font-weight: 600;
      font-size: 0.95rem;
      color: #e2e8f0;
      margin-bottom: 4px;
    }
    .result-item .snippet {
      font-size: 0.82rem;
      color: #94a3b8;
      margin-bottom: 8px;
      line-height: 1.5;
    }
    .result-item a {
      font-size: 0.8rem;
      color: #38bdf8;
      text-decoration: none;
      word-break: break-all;
    }
    .result-item a:hover { text-decoration: underline; }

    .buy-item {
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 12px 16px;
      margin-bottom: 10px;
      transition: background 0.2s;
    }
    .buy-item:hover { background: rgba(255,255,255,0.08); }
    .buy-item img {
      width: 44px; height: 44px;
      object-fit: contain;
      border-radius: 6px;
      background: rgba(255,255,255,0.06);
      flex-shrink: 0;
    }
    .buy-item .info { flex: 1; min-width: 0; }
    .buy-item .info .title {
      font-weight: 600;
      font-size: 0.9rem;
      color: #e2e8f0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .buy-item .info .source {
      font-size: 0.78rem;
      color: #64748b;
      margin-top: 2px;
    }
    .buy-item .price {
      font-weight: 700;
      color: #4ade80;
      font-size: 0.95rem;
      flex-shrink: 0;
    }
    .buy-item a.buy-link {
      display: inline-block;
      padding: 7px 14px;
      background: linear-gradient(135deg, #4ade80, #22d3ee);
      border-radius: 7px;
      color: #0f172a;
      font-size: 0.78rem;
      font-weight: 700;
      text-decoration: none;
      flex-shrink: 0;
      transition: opacity 0.2s;
    }
    .buy-item a.buy-link:hover { opacity: 0.85; }

    .empty-state {
      text-align: center;
      color: #475569;
      font-size: 0.9rem;
      padding: 20px 0;
    }
    .badge {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 99px;
      font-size: 0.72rem;
      font-weight: 700;
      background: rgba(129,140,248,0.15);
      color: #a5b4fc;
      margin-left: 8px;
      vertical-align: middle;
    }
  </style>
</head>
<body>

  <div class="header">
    <h1>&#128138; Medicine Alternatives Finder</h1>
    <p>Enter a medicine name and your SerpAPI key to discover alternatives and buy online.</p>
  </div>

  <div class="card">
    <!-- SerpAPI Key -->
    <div class="form-group">
      <label>SerpAPI Key</label>
      <div class="key-row">
        <div class="form-group">
          <input type="password" id="apiKey" placeholder="Enter your SerpAPI key…" autocomplete="off" />
        </div>
        <button class="toggle-btn" onclick="toggleKey()" title="Show/Hide key">&#128065;</button>
      </div>
    </div>

    <!-- Medicine Name -->
    <div class="form-group">
      <label>Medicine Name</label>
      <input type="text" id="medicineName" placeholder="e.g. Paracetamol, Amoxicillin, Metformin…" />
    </div>

    <button class="search-btn" id="searchBtn" onclick="findAlternatives()">
      &#128269; Find Alternatives
    </button>

    <div class="spinner" id="spinner">
      <div class="spinner-ring"></div>
      <p style="margin-top:12px;color:#64748b;font-size:0.85rem;">Searching Google via SerpAPI…</p>
    </div>

    <div class="error-box" id="errorBox"></div>
  </div>

  <div class="card results" id="results" style="display:none; margin-top:20px;">
    <!-- Alternatives pills -->
    <div class="section-title">
      Alternative Medicines <span id="altCount" class="badge"></span>
    </div>
    <div class="alt-grid" id="altGrid"></div>

    <!-- Organic results -->
    <div class="section-title">
      Detailed Results <span id="orgCount" class="badge"></span>
    </div>
    <ul class="result-list" id="organicList"></ul>

    <!-- Purchase links -->
    <div class="section-title" style="margin-top: 24px;">
      Where to Buy <span id="buyCount" class="badge"></span>
    </div>
    <div id="buyList"></div>
  </div>

  <script>
    document.getElementById('medicineName').addEventListener('keydown', e => {
      if (e.key === 'Enter') findAlternatives();
    });
    document.getElementById('apiKey').addEventListener('keydown', e => {
      if (e.key === 'Enter') findAlternatives();
    });

    function toggleKey() {
      const inp = document.getElementById('apiKey');
      inp.type = inp.type === 'password' ? 'text' : 'password';
    }

    function setLoading(on) {
      document.getElementById('spinner').style.display = on ? 'block' : 'none';
      document.getElementById('searchBtn').disabled = on;
      document.getElementById('searchBtn').textContent = on ? 'Searching…' : '🔍 Find Alternatives';
    }

    function showError(msg) {
      const box = document.getElementById('errorBox');
      box.textContent = '⚠️  ' + msg;
      box.style.display = 'block';
    }

    function hideError() {
      document.getElementById('errorBox').style.display = 'none';
    }

    async function findAlternatives() {
      const medicine = document.getElementById('medicineName').value.trim();
      const apiKey   = document.getElementById('apiKey').value.trim();

      hideError();
      document.getElementById('results').style.display = 'none';

      if (!medicine) { showError('Please enter a medicine name.'); return; }
      if (!apiKey)   { showError('Please enter your SerpAPI key.'); return; }

      setLoading(true);
      try {
        const resp = await fetch('/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ medicine, api_key: apiKey })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.error || 'Request failed');
        renderResults(data, medicine);
      } catch (err) {
        showError(err.message);
      } finally {
        setLoading(false);
      }
    }

    function renderResults(data, medicine) {
      const { alternatives = [], organic = [], purchase = [] } = data;

      const altGrid = document.getElementById('altGrid');
      altGrid.innerHTML = '';
      document.getElementById('altCount').textContent = alternatives.length;
      if (alternatives.length) {
        alternatives.forEach(name => {
          const pill = document.createElement('div');
          pill.className = 'alt-pill';
          pill.textContent = name;
          altGrid.appendChild(pill);
        });
      } else {
        altGrid.innerHTML = '<p class="empty-state">No specific alternatives extracted — see detailed results below.</p>';
      }

      const orgList = document.getElementById('organicList');
      orgList.innerHTML = '';
      document.getElementById('orgCount').textContent = organic.length;
      if (organic.length) {
        organic.forEach(r => {
          const li = document.createElement('li');
          li.className = 'result-item';
          li.innerHTML = `
            <div class="title">${escHtml(r.title)}</div>
            ${r.snippet ? `<div class="snippet">${escHtml(r.snippet)}</div>` : ''}
            <a href="${escHtml(r.link)}" target="_blank" rel="noopener">${escHtml(r.link)}</a>
          `;
          orgList.appendChild(li);
        });
      } else {
        orgList.innerHTML = '<p class="empty-state">No organic results found.</p>';
      }

      const buyList = document.getElementById('buyList');
      buyList.innerHTML = '';
      document.getElementById('buyCount').textContent = purchase.length;
      if (purchase.length) {
        purchase.forEach(p => {
          const div = document.createElement('div');
          div.className = 'buy-item';
          div.innerHTML = `
            ${p.thumbnail ? `<img src="${escHtml(p.thumbnail)}" alt="" />` : ''}
            <div class="info">
              <div class="title">${escHtml(p.title)}</div>
              <div class="source">${escHtml(p.source || p.link)}</div>
            </div>
            ${p.price ? `<div class="price">${escHtml(p.price)}</div>` : ''}
            <a class="buy-link" href="${escHtml(p.link)}" target="_blank" rel="noopener">Buy</a>
          `;
          buyList.appendChild(div);
        });
      } else {
        buyList.innerHTML = '<p class="empty-state">No purchase links found.</p>';
      }

      document.getElementById('results').style.display = 'block';
      document.getElementById('results').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function escHtml(str) {
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }
  </script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# SerpAPI helpers
# ---------------------------------------------------------------------------

SERPAPI_URL = "https://serpapi.com/search"

MEDICINE_STOP_WORDS = {
    "alternative", "alternatives", "substitute", "substitutes", "generic",
    "generics", "similar", "equivalent", "equivalents", "drugs", "drug",
    "medicine", "medicines", "medication", "medications", "brand", "brands",
    "over", "counter", "otc", "prescription", "best", "list", "top", "common",
    "and", "or", "the", "of", "for", "to", "a", "an", "in", "is", "are",
    "with", "vs", "versus", "compared", "other", "these", "those", "which",
    "what", "how", "why", "when", "where", "that", "this", "also", "can",
    "may", "might", "should", "would", "could", "your", "you", "use",
    "used", "using", "help", "helps", "effective", "safe", "treat",
    "treatment", "condition", "pain", "relief", "mg", "ml", "dose",
}


def call_serpapi(query: str, api_key: str, extra_params: dict = None) -> dict:
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 10,
        "hl": "en",
        "gl": "us",
    }
    if extra_params:
        params.update(extra_params)

    resp = requests.get(SERPAPI_URL, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def extract_medicine_names(medicine: str, data: dict) -> list[str]:
    names: list[str] = []
    seen: set[str] = {medicine.lower()}

    def add(candidate: str):
        c = candidate.strip().strip(".,;:-")
        if not c or len(c) < 3:
            return
        if c.lower() in seen:
            return
        if c.lower() in MEDICINE_STOP_WORDS:
            return
        seen.add(c.lower())
        names.append(c)

    answer_box = data.get("answer_box", {})
    for key in ("list", "result", "answer"):
        val = answer_box.get(key)
        if isinstance(val, list):
            for item in val:
                add(str(item))
        elif isinstance(val, str):
            add(val)

    for rs in data.get("related_searches", []):
        query_str = rs.get("query", "")
        words = query_str.split()
        if 1 <= len(words) <= 4:
            candidate = " ".join(w for w in words if w.lower() not in MEDICINE_STOP_WORDS)
            if candidate:
                add(candidate)

    import re
    for result in data.get("organic_results", [])[:8]:
        title = result.get("title", "")
        for match in re.findall(r'["\u201c\u201d]([^"\u201c\u201d]{3,40})["\u201c\u201d]', title):
            add(match)
        for token in title.split():
            clean = re.sub(r"[^a-zA-Z0-9-]", "", token)
            if (
                clean
                and len(clean) >= 4
                and clean.lower() not in MEDICINE_STOP_WORDS
                and clean.lower() != medicine.lower()
                and (clean[0].isupper() or clean.isupper())
                and not clean.isnumeric()
            ):
                add(clean)

    return names[:20]


def extract_organic(data: dict) -> list[dict]:
    results = []
    for r in data.get("organic_results", []):
        results.append({
            "title": r.get("title", ""),
            "snippet": r.get("snippet", ""),
            "link": r.get("link", ""),
        })
    return results


def extract_purchase(alt_data: dict, buy_data: dict) -> list[dict]:
    purchase = []
    seen_links: set[str] = set()

    def add_item(item: dict):
        link = item.get("link") or item.get("product_link", "")
        if not link or link in seen_links:
            return
        seen_links.add(link)
        purchase.append({
            "title": item.get("title", ""),
            "link": link,
            "price": item.get("price", ""),
            "source": item.get("source", ""),
            "thumbnail": item.get("thumbnail", ""),
        })

    for s in alt_data.get("shopping_results", []):
        add_item(s)

    for s in buy_data.get("shopping_results", []):
        add_item(s)

    for s in buy_data.get("inline_shopping_results", []):
        add_item(s)

    pharmacy_keywords = {
        "amazon", "walmart", "cvs", "walgreens", "pharmacy", "chemist",
        "drug", "health", "medline", "netmeds", "1mg", "pharmeasy",
        "apollo", "flipkart", "shop", "buy", "store", "online",
    }
    for r in buy_data.get("organic_results", [])[:6]:
        link = r.get("link", "")
        title = r.get("title", "").lower()
        domain = r.get("displayed_link", "").lower()
        if any(kw in title or kw in domain for kw in pharmacy_keywords):
            add_item({
                "title": r.get("title", ""),
                "link": link,
                "price": "",
                "source": r.get("displayed_link", ""),
                "thumbnail": "",
            })

    return purchase[:15]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/search", methods=["POST"])
def search():
    body = request.get_json(force=True, silent=True) or {}
    medicine: str = (body.get("medicine") or "").strip()
    api_key: str  = (body.get("api_key") or "").strip()

    if not medicine:
        return jsonify({"error": "Medicine name is required."}), 400
    if not api_key:
        return jsonify({"error": "SerpAPI key is required."}), 400

    try:
        alt_query = f"{medicine} medicine alternatives generic substitutes equivalent drugs"
        alt_data = call_serpapi(alt_query, api_key)

        buy_query = f"buy {medicine} medicine online pharmacy"
        buy_data = call_serpapi(buy_query, api_key, {"tbm": "shop"})

        buy_organic_data = call_serpapi(buy_query, api_key)

        buy_data.setdefault("organic_results", [])
        buy_data["organic_results"].extend(buy_organic_data.get("organic_results", []))
        buy_data.setdefault("shopping_results", [])
        buy_data["shopping_results"].extend(buy_organic_data.get("shopping_results", []))

        return jsonify(
            {
                "alternatives": extract_medicine_names(medicine, alt_data),
                "organic": extract_organic(alt_data),
                "purchase": extract_purchase(alt_data, buy_data),
            }
        )

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else 0
        if status == 401:
            return jsonify({"error": "Invalid SerpAPI key. Please check and try again."}), 400
        if status == 429:
            return jsonify({"error": "SerpAPI rate limit reached. Please wait and try again."}), 429
        return jsonify({"error": f"SerpAPI error: {e}"}), 502
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Could not connect to SerpAPI. Check your internet connection."}), 502
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to SerpAPI timed out. Please try again."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n  Medicine Alternatives Finder")
    print("  ─────────────────────────────────────────")
    print("  Open in your browser: http://localhost:5000")
    print("  Press Ctrl+C to stop.\n")
    app.run(debug=False, port=5000)
