FROM python:3.12-slim-bookworm

WORKDIR /code
# COPY ./src ./code/


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./code/

# Fix for FastAI
# RUN pip uninstall numpy
RUN pip install "numpy<2"
RUN pip install gunicorn

CMD ["gunicorn" "src.web.app:app" "-w" "2" "--threads" "2" "-b" "0.0.0.0:3000"]
