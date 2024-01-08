FROM python:3.9

WORKDIR /app

COPY cfproxy.py /app/cfproxy.py
COPY dbmanager.py /app/dbmanager.py
COPY requirements.txt /app/requirements.txt

ENV CFPROXY_CFBASE='/tmp'
RUN pip install -r requirements.txt && chmod -R +x /app

EXPOSE 5000

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["sh", "-c", "/app/entrypoint.sh"]
