FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install library
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy semua file kamu (app.py, dataset) ke dalam server
COPY . .

# Hugging Face Spaces pakai port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]