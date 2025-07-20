FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt ./
RUN python -m venv .venv \
&& source .venv/bin/activate \
&& pip install --no-cache-dir -r requirements.txt
ADD src ./
RUN adduser user --disabled-password --no-create-home --gecos ""
USER user
CMD ["/app/.venv/bin/python", "./main.py"]

