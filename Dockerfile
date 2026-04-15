# Use Python 3.11 slim (smaller image)
FROM python:3.11-slim
# Set working directory inside container
WORKDIR /app
# Copy requirements.txt
COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
#set nltk path
ENV NLTK_DATA=/usr/local/share/nltk_data
# Install NLTK data (needed by e2k/g2p_en)
RUN python -m nltk.downloader punkt averaged_perceptron_tagger cmudict -d /usr/local/share/nltk_data
# Copy entire project
COPY . .
# Expose port 5000
EXPOSE 5000
# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "pyApp:app"]
