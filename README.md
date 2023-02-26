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