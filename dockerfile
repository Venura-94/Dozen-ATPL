# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install python packages
RUN pip install -r requirements.txt

# for streamlit
EXPOSE 8501

# Run main.py when the container launches
CMD ["streamlit", "run", "streamlit_app.py"]

# don't forget to add the .env file if running docker locally
# docker build -t atpl .
# docker run -p 800:8501 atpl (map 8501 port to 800 outside)