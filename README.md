# PKI-Based 2FA Microservice

Secure authentication microservice using RSA encryption and TOTP-based 2FA, deployed with Docker.

## Features
- 4096-bit RSA key pair (student keys)
- RSA/OAEP seed decryption
- TOTP-based 2FA generation & verification
- FastAPI backend with 3 endpoints
- Persistent storage via Docker volumes
- Cron job that logs 2FA codes every minute

##  API Endpoints
- POST /decrypt-seed     — Decrypt the encrypted seed
- GET /generate-2fa      — Generate current TOTP code
- POST /verify-2fa       — Verify submitted TOTP code

##  Tech Stack
 FastAPI · Cryptography · PyOTP · Docker · Docker Compose

## Setup & Commands
```bash
#  Generate RSA keys
python generate_keys.py

#  Download instructor public key
curl -o instructor_public.pem <instructor-api-url>

#  Request encrypted seed
python request_seed.py

#  Build and run Docker container
docker-compose up --build



