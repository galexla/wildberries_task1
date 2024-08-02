FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY teams /app/

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl -sS 127.0.0.1:8000 || exit 1

CMD ["gunicorn", "teams.wsgi:application", "--bind", "0.0.0.0:8000"]
