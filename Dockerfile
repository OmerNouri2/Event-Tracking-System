# Use official Python image
FROM python:3.10

# Install netcat (nc) for wait-for-it.sh   # cannot add netcat to your Python requirements because it's not a Python package—it's a system utility.
RUN apt-get update && apt-get install -y netcat-openbsd

# Set working directory in the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Copy the tests folder separately (to avoid any issues)
COPY tests /app/tests

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure wait-for-it.sh has executable permissions
RUN chmod +x wait-for-it.sh

# Run the FastAPI application  (without tests)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Run the tests before starting the FastAPI app
# CMD pytest && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
