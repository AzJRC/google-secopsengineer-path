# Use official Python base image
FROM python:3.12-bookworm

# Install dependencies
RUN pip install flask

# Set working directory
WORKDIR /vuln_app

# Copy app files
COPY vuln_app.py /vuln_app/vuln_app.py
COPY templates /vuln_app/templates

# Expose the port Flask runs on
EXPOSE 8080

# Set entrypoint
CMD ["python", "/vuln_app/vuln_app.py"]
