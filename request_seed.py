import requests
import json

api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

student_id = "23A91A05H7"
github_repo_url = "https://github.com/palaparthisupriya/Secure-auth-Gpp"

# Read the raw public key
with open("student_public.pem", "r") as f:
    public_key = f.read()  # KEEP line breaks intact

payload = {
    "student_id": student_id,
    "github_repo_url": github_repo_url,
    "public_key": public_key
}

headers = {"Content-Type": "application/json"}

response = requests.post(api_url, data=json.dumps(payload), headers=headers)

print("Status:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    encrypted_seed = response.json().get("encrypted_seed", "")
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)
    print("Encrypted seed saved to encrypted_seed.txt")
