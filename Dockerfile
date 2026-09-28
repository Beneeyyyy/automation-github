# ── Base image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# ── System deps + Chromium ────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    # fonts & display libs needed by headless Chromium
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    wget \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ── Copy chromedriver to a writable location (needed by undetected-chromedriver) ──
RUN cp /usr/bin/chromedriver /usr/local/bin/chromedriver-uc \
    && chmod 777 /usr/local/bin/chromedriver-uc

# ── App ───────────────────────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ── Run ───────────────────────────────────────────────────────────────────────
CMD ["python", "bot.py"]
