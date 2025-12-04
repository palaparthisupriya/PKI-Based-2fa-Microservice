import subprocess
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import json

def get_commit_hash():
    """Get the current commit hash from git"""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Could not get commit hash. Make sure you're in a git repository.")
        return None

def sign_commit_hash(commit_hash):
    """Sign the commit hash using RSA-PSS with SHA-256"""
    try:
        # Read the private key
        with open('student_private.pem', 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=None)
        
        # Sign the commit hash using RSA-PSS with SHA-256
        signature = private_key.sign(
            commit_hash.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Encode signature as base64
        encoded_signature = base64.b64encode(signature).decode('utf-8')
        return encoded_signature
    except FileNotFoundError:
        print("Error: student_private.pem not found")
        return None
    except Exception as e:
        print(f"Error signing commit hash: {e}")
        return None

def verify_submission_files():
    """Verify that all required files exist"""
    required_files = ['student_public.pem', 'encrypted_seed.txt']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    return missing_files

def main():
    print("[*] Generating submission proof...")
    print()
    
    # Check for required files
    missing = verify_submission_files()
    if missing:
        print(f"[X] Error: Missing files: {', '.join(missing)}")
        print("    Please ensure you have completed STEP 1 (request_seed.py)")
        return False
    
    print("[+] All required files found")
    print()
    
    # Get commit hash
    commit_hash = get_commit_hash()
    if not commit_hash:
        print("[X] Error: Could not get commit hash")
        return False
    
    print(f"[+] Current commit hash: {commit_hash}")
    print()
    
    # Sign the commit hash
    print("[*] Signing commit hash with RSA-PSS (SHA-256)...")
    encrypted_signature = sign_commit_hash(commit_hash)
    if not encrypted_signature:
        print("[X] Error: Could not sign commit hash")
        return False
    
    print(f"[+] Signature generated successfully")
    print()
    
    # Read student public key
    print("[*] Reading student public key...")
    with open('student_public.pem', 'r') as f:
        student_public_key = f.read()
    print("[+] Student public key loaded")
    print()
    
    # Read encrypted seed
    print("[*] Reading encrypted seed...")
    with open('encrypted_seed.txt', 'r') as f:
        encrypted_seed = f.read()
    print("[+] Encrypted seed loaded")
    print()
    
    print("=" * 70)
    print("SUBMISSION DATA - Copy these values to Partnr")
    print("=" * 70)
    print()
    
    print("1. GitHub Repository URL:")
    print("   https://github.com/MadhavaKandala/pki-2fa-microservice")
    print()
    
    print("2. Commit Hash:")
    print(f"   {commit_hash}")
    print()
    
    print("3. Encrypted Commit Signature:")
    print(f"   {encrypted_signature}")
    print()
    
    print("4. Student Public Key:")
    print(student_public_key)
    print()
    
    print("5. Encrypted Seed:")
    print(encrypted_seed)
    print()
    
    print("=" * 70)
    print("All data is ready for submission on Partnr!")
    print("=" * 70)
    
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)