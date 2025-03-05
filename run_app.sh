# The error occurs because httpx (used by astrapy) is trying to create an SSL context using the certificate file path specified by the environment variable SSL_CERT_FILE. If this variable is set to an invalid path (or even an empty string), then when Python calls ssl.create_default_context(cafile=...) it fails with an "Invalid argument" error.
# setting SSL_CERT_FILE to a correct path and note : The SSL_CERT_FILE variable should point to a specific certificate file (typically a PEM file) rather than a directory.
SSL_CERT_FILE="C:\Users\soman\anaconda3\envs\fastapi_astradb\Library\ssl\cert.pem"

# run server, --reload flag is for auto-reload after changes in development
uvicorn app.main:app  --reload 