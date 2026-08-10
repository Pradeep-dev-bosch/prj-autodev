FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY gerritmcpserver.py .

RUN uv pip install --system -e .

ENV TRANSPORT=stdio

CMD ["python", "gerritmcpserver.py"]
