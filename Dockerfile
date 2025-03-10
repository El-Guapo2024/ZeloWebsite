FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

EXPOSE 5000

# Command to run the Flask app
CMD ["gunicorn", "-w", "4" , "-b", "0.0.0.0:5000", "app:create_app()"]
