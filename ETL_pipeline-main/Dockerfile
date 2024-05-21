FROM python:3.9

# Set the working directory inside the container
WORKDIR /code
 
# Define a volume for the /dataset directory
VOLUME /dataset 

# Copy the requirements.txt file into the container at /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt
 
# Install the required Python packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
# Copy the contents of the app directory into the container at /code/app
COPY ./app /code/app
 
# Set the default command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]