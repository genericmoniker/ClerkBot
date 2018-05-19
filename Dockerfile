FROM python:3

# Create the app directory.
WORKDIR /app

# Copy all the (non-ignored) files to the app directory.
COPY . .

# Install dependencies and the project itself.
RUN pip install -r requirements.txt
RUN pip install .
