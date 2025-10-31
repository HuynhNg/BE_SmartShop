# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Cài đặt các dependency hệ thống (bao gồm Microsoft ODBC Driver 17)
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    unixodbc \
    unixodbc-dev

# Thêm Microsoft repository và cài ODBC Driver 17 (Debian 12 không còn apt-key)
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copy requirements và cài Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8080

# Run the app
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8080"]
