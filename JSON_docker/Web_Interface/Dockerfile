FROM python:3.11-slim

WORKDIR /app

COPY Web_Interface/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Parent-level modules web_main.py imports via sys.path
COPY *.py .

# Web interface source (only what's needed — venv is not copied)
# COPY Web_Interface/static/ Web_Interface/static/
# COPY Web_Interface/web_main.py Web_Interface/
# Web interface source
COPY Web_Interface/ Web_Interface/

WORKDIR /app/Web_Interface

CMD ["uvicorn", "web_main:app", "--host", "0.0.0.0", "--port", "8000"]
