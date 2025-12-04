#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import pyotp
import base64

try:
    with open('/data/seed.txt', 'r') as f:
        seed = f.read().strip()
    
    seed_bytes = bytes.fromhex(seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    code = totp.now()
    
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"{timestamp} - 2FA Code: {code}\n"
    
    os.makedirs('/cron', exist_ok=True)
    with open('/cron/last_code.txt', 'a') as f:
        f.write(log_line)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)