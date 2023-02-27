# YouTube Data Extractor

This directory contains extractor to get data from YouTube.

## Local Set Up
Below you find instruction how to correctly set up your local environment for this extractor.

### Google Cloud Set Up 
1. Login to your Google Cloud account, create or select any existing project. 
2. Select `API & Services` from side menu and then go to `Library` panel.
3. Using searchbar find `YouTube Data API v3` and then enable it for your project.
4. Switch to `Credentials` panel:
   - Create an API Key and put it value in .env file as `GOOGLE_CLOUD_API_KEY`.
   - Create an OAuth 2.0 client ID 

### Create virtual environment
1. Create virtual environment using Python's `venv` module:
   ```shell
   python3 -m venv venv 
   ```
2. Install all dependencies from `requirements.txt` file:
   ```shell
   pip install -r requirements.txt
   ```

### Build a Docker image
1. Create `.env` file by executing: 
   ```shell
   cp dev.env .env
   ```
2. Provide values for all env variables in file `.env`
3. 

## Possible debugging 
### Installing psycopg2 on MacBook with M1 chip
1. Install openssl by running command:
    ```shell
    brew install openssl
    ```
2. Check the path where openssl is installed:
    ```shell
    brew --prefix openssl
    ```
3. Use output from above and add LD flag when running the pip command. For example if the output is `/opt/homebrew/opt/openssl@1.1` run command below:
    ```shell
    LDFLAGS="-I/opt/homebrew/opt/openssl@1.1/include -L/opt/homebrew/opt/openssl@1.1/lib" pip install psycopg2
    ```