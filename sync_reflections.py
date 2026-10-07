import os
import re
import glob

REPO_DIR = os.path.dirname(os.path.abspath(__file__))
REFLECTIONS_DIR = os.path.join(REPO_DIR, "reflections")

# Define all 13 reflection weeks
WEEKS = [f"week{i:02d}" for i in range(1, 14)]

def parse_reflection_md(filepath):
    if not os.path.exists(filepath):
        return "", ""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.strip().split("\n")
    prompt = ""
    paragraphs = []
    found_prompt = False
    current_para = []

    for line in lines:
        stripped = line.strip()
        if not found_prompt and (stripped.startswith("Reflect ") or re.search(r"Reflect\s+\d+:", stripped)):
            prompt_match = re.search(r"Reflect\s+\d+:\s*(.*)", stripped)
            if prompt_match:
                prompt = prompt_match.group(1).strip()
            else:
                prompt = stripped
            found_prompt = True
            continue

        if found_prompt:
            # Skip any markdown help or headers if present
            if stripped.startswith(">") or stripped.startswith("#"):
                continue
            if stripped:
                current_para.append(stripped)
            else:
                if current_para:
                    paragraphs.append(" ".join(current_para))
                    current_para = []

    if current_para:
        paragraphs.append(" ".join(current_para))

    return prompt, paragraphs

def build_reflection_html(week_id, num, prompt, paragraphs, prev_week, next_week):
    prev_top = f'<a href="{prev_week}.html" class="btn-cute btn-secondary" style="font-size: 0.85rem; padding: 6px 14px;">← Week {int(prev_week[-2:])}</a>' if prev_week else '<span style="font-size: 0.85rem; color: var(--text-muted); opacity: 0.5;">← First Week</span>'
    next_top = f'<a href="{next_week}.html" class="btn-cute btn-secondary" style="font-size: 0.85rem; padding: 6px 14px;">Week {int(next_week[-2:])} →</a>' if next_week else '<span style="font-size: 0.85rem; color: var(--text-muted); opacity: 0.5;">Final Week →</span>'

    prev_bottom = f'<a href="{prev_week}.html" class="btn-cute btn-secondary">← Week {int(prev_week[-2:])}</a>' if prev_week else '<div></div>'
    next_bottom = f'<a href="{next_week}.html" class="btn-cute btn-secondary">Week {int(next_week[-2:])} →</a>' if next_week else '<div></div>'

    if paragraphs:
        paras_html = "\n".join([
            f'        <p style="margin-bottom: 16px; line-height: 1.7; color: var(--text-main); font-size: 1rem;">\n          {p}\n        </p>'
            for p in paragraphs
        ])
    else:
        paras_html = """        <p style="color: var(--text-muted); font-style: italic; margin-bottom: 0;">
          Draft or view your weekly critical response here (approx. 200–300 words). Connect the readings, classroom discussions, and practical experiments to the core questions raised by the prompt.
        </p>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week {num} Reflection | DH101 | Maddie Jensen</title>
  <link rel="stylesheet" href="../assets/css/style.css">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>📝</text></svg>">
  <script>
    (function() {{
      try {{
        var saved = localStorage.getItem('maddie_space_theme');
        var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        var theme = saved || (prefersDark ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme);
      }} catch (e) {{}}
    }})();
  </script>
</head>
<body>
  <!-- Navigation Header -->
  <nav class="cute-nav">
    <div class="cute-nav-inner">
      <a href="../index.html" class="cute-brand">
        <span class="brand-sparkle">✨</span> Maddie's Space 🌸
      </a>
      <ul class="nav-links">
        <li><a href="../index.html">🏠 Home</a></li>
        <li><a href="../index.html#angel">🐾 Angel Baby</a></li>
        <li><a href="../index.html#resume">📄 Resume</a></li>
        <li><a href="../pages/about.html">🌸 About</a></li>
        <li><a href="../index.html#coursework" class="active">📚 DH101</a></li>
      </ul>
      <button id="themeToggle" class="theme-toggle" type="button" aria-label="Toggle theme" title="Toggle theme">
        <span class="theme-toggle-icon" aria-hidden="true">🌙</span>
        <span class="theme-toggle-text">Dark</span>
      </button>
    </div>
  </nav>

  <main class="container">
    <article class="markdown-content">
      <div style="text-align: center; margin-bottom: 24px;">
        <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-bottom: 12px;">
          <span class="badge badge-lavender">📝 Weekly Reflection {num}</span>
          <span class="badge badge-pink">DH101 • Fall 2025</span>
          <span class="badge badge-mint">Denison University 🌸</span>
        </div>
        <h1 style="border: none; padding: 0; margin-bottom: 8px;">Week {num} Reflection</h1>
        <p style="color: var(--text-muted); font-size: 1.05rem;">
          Critical Inquiry, Theoretical Connections &amp; Seminar Reflection
        </p>
      </div>

      <!-- Quick Subnav: Prev, Hub, Next -->
      <div style="display: flex; gap: 10px; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 30px; padding: 10px 16px; background: var(--bg-card-alt); border-radius: var(--radius-md); border: 1px dashed var(--border-soft);">
        <div>
          {prev_top}
        </div>
        <div>
          <a href="../index.html#coursework" class="btn-cute btn-secondary" style="font-size: 0.85rem; padding: 6px 14px;">📚 DH101 Hub</a>
        </div>
        <div>
          {next_top}
        </div>
      </div>

      <h2>Reflection Prompt</h2>
      <blockquote>
        "{prompt}"
      </blockquote>

      <h2>My Reflection</h2>
      <div class="cute-card" style="margin-bottom: 24px;">
{paras_html}
      </div>

      <!-- Bottom Navigation -->
      <div style="margin-top: 48px; padding-top: 24px; border-top: 2px dashed var(--border-soft); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        {prev_bottom}
        <a href="../index.html#coursework" class="btn-cute btn-primary">🌸 Back to DH101 Hub</a>
        {next_bottom}
      </div>
    </article>
  </main>

  <footer class="cute-footer">
    <div class="container">
      <p>Made with <span class="footer-heart">💖</span> and lots of treats for Angel Baby 🐾</p>
      <p><small>© 2026 Madison Jensen • Denison University • Digital Humanities 101</small></p>
    </div>
  </footer>
  <script src="../assets/js/theme.js"></script>
</body>
</html>
"""
    return html

def sync_all():
    for i, w in enumerate(WEEKS):
        num = i + 1
        md_path = os.path.join(REFLECTIONS_DIR, f"{w}.md")
        html_path = os.path.join(REFLECTIONS_DIR, f"{w}.html")
        prev_w = WEEKS[i-1] if i > 0 else None
        next_w = WEEKS[i+1] if i < len(WEEKS) - 1 else None

        prompt, paragraphs = parse_reflection_md(md_path)
        html = build_reflection_html(w, num, prompt, paragraphs, prev_w, next_w)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated {html_path} ({len(paragraphs)} reflection paragraphs)")

if __name__ == "__main__":
    sync_all()
