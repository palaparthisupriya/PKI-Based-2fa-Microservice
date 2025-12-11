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
            private_key = serialization.load_pem_private_key(
                f.read(), password=None
            )
        
        # Sign commit hash
        signature = private_key.sign(
            commit_hash.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('utf-8')

    except Exception as e:
        print(f"Error signing commit hash: {e}")
        return None

def verify_submission_files():
    required_files = ['student_public.pem', 'encrypted_seed.txt']
    missing = [f for f in required_files if not Path(f).exists()]
    return missing

def main():
    print("[*] Generating submission proof...\n")
    
    missing = verify_submission_files()
    if missing:
        print(f"[X] Missing files: {', '.join(missing)}")
        return False
    
    commit_hash = get_commit_hash()
    if not commit_hash:
        return False
    
    print(f"[+] Commit hash: {commit_hash}\n")
    
    print("[*] Signing commit hash...")
    signature = sign_commit_hash(commit_hash)
    if not signature:
        return False
    
    print("[+] Signature created\n")

    with open('student_public.pem', 'r') as f:
        pubkey = f.read()

    with open('encrypted_seed.txt', 'r') as f:
        encrypted_seed = f.read()

    print("=" * 70)
    print("SUBMISSION DATA (paste these in Partnr)")
    print("=" * 70)

    print("\n1. GitHub Repository URL:")
    print("   https://github.com/palaparthisupriya/PKI-Based-2fa-Microservice")

    print("\n2. Commit Hash:")
    print(f"   {commit_hash}")

    print("\n3. Encrypted Commit Signature:")
    print(f"   {signature}")

    print("\n4. Student Public Key:")
    print(pubkey)

    print("\n5. Encrypted Seed:")
    print(encrypted_seed)

    print("=" * 70)
    return True

if __name__ == '__main__':
    exit(0 if main() else 1)
