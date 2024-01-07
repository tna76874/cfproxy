FROM python:3.9

WORKDIR /app

COPY cfproxy.py /app/cfproxy.py
COPY dbmanager.py /app/dbmanager.py
COPY requirements.txt /app/requirements.txt

ENV CFPROXY_CFBASE='/app'
RUN pip install -r requirements.txt && quickflare --download --path /app && chmod -R +x /app

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "cfproxy:app"]
