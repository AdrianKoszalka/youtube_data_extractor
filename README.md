# YouTube Data Extractor

This repository contains an extractor designed to retrieve data from YouTube.

## Local Setup
Below are instructions for properly setting up your local environment for this extractor.

### Google Cloud Setup
1. Login to your Google Cloud account and create or select an existing project.
2. Select `API & Services` from the side menu, and then go to the `Library` panel.
3. Use the search bar to find `YouTube Data API v3` and enable it for your project.
4. Switch to `Credentials` panel:
   - Create an API Key and add its value to the .env file as `GOOGLE_CLOUD_API_KEY`.
   - Create an OAuth 2.0 client ID.

### Create a Virtual Environment
1. Create a virtual environment using Python's `venv` module:
   ```shell
   python3 -m venv venv 
   ```
2. Install all dependencies from the `requirements.txt` file:
   ```shell
   pip install -r requirements.txt
   ```

### Build a Docker Image
1. Create `.env` file by executing: 
   ```shell
   cp dev.env .env
   ```
2. Provide values for all environment variables in the `.env` file.
3. From the root repository, build a Docker image by running the following command:
   ```shell
   docker build -t youtube_data_extractor:latest .
   ```

### Run the Docker Image
To run the Docker image, execute the command below:
```shell
docker run -rm --env-file .env youtube_data_extractor:latest --channel_id={channel_id}
```

## Possible Debugging 
### Installing psycopg2 on a MacBook with an M1 chip
1. Install OpenSSL by running the command:
    ```shell
    brew install openssl
    ```
2. Check the path where OpenSSL is installed:
    ```shell
    brew --prefix openssl
    ```
3. Use the output from above and add LD flag when running the pip command. For example, if the output is `/opt/homebrew/opt/openssl@1.1`, run the command below:
    ```shell
    LDFLAGS="-I/opt/homebrew/opt/openssl@1.1/include -L/opt/homebrew/opt/openssl@1.1/lib" pip install psycopg2
    ```