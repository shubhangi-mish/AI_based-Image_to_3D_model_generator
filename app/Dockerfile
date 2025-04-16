FROM openfabric/tee-python-cpu:dev

# Copy only necessary files for Poetry installation
COPY pyproject.toml ./

# Install dependencies using Poetry
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade poetry && \
    python3 -m poetry install --only main && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts}

# Copy the rest of the source code into the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 8888

# Start the Flask app using the start.sh script
CMD ["sh","start.sh"]