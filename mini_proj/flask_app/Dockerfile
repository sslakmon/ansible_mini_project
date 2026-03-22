FROM python:3.11-slim

WORKDIR /app

# Install Flask and psycopg2
RUN pip install Flask psycopg2-binary

# Copy the application
COPY . .

EXPOSE 5000

HEALTHCHECK --interval=10s --timeout=3s \
  CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "app.py"]
