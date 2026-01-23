FROM python:3.13
#FROM docker.1ms.run/library/python:3.13

WORKDIR /app

ENV ENV_FILE=docker \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY requirements.txt .

RUN python -m venv $VIRTUAL_ENV && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY . .

RUN ls -l /app/

EXPOSE 9990

CMD ["python", "/app/main.py", "run"]