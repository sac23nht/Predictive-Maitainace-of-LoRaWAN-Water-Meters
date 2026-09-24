FROM python:3.10-slim

WORKDIR /app

# System deps needed to build some scientific-python wheels on slim images
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY src/ src/
COPY .streamlit/ .streamlit/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:${PORT:-8501}/_stcore/health || exit 1

# Most container platforms (Render, Railway, Fly.io, etc.) inject $PORT;
# fall back to Streamlit's default 8501 for local `docker run`.
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]
