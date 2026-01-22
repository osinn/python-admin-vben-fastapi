FROM python:3.13
#FROM docker.1ms.run/library/python:3.13

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV ENV_FILE=docker
ENV PYTHONUNBUFFERED=1

COPY . .

RUN python -m venv /app/.venv

RUN . /app/.venv/bin/activate

ENV PATH="/app/.venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 暴露FastAPI默认端口（根据你的main.py实际端口调整）
EXPOSE 9990
CMD ["python", "main.py", "run"]