FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Create and populate a venv on the HOST machine
# (Mounted volume will persist after container exits)
RUN python3.11 -m venv /app/venv3 \
    && . /app/venv3/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Copy the script (optional, since we'll mount it later)
COPY wazeScraper.py .

# Set a script to auto-run when container starts
CMD ["bash", "-c", "source /app/venv3/bin/activate && python /app/wazeScraper.py"]