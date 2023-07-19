# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /src
# Copy the current directory contents into the container at /app
COPY . /src/
# Copy the requirements.txt file first to take advantage of Docker's build caching
COPY requirements.txt /src/
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make migrations   
RUN python manage.py makemigrations
# Apply migrations  
RUN python manage.py migrate

# Make port 8000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]    