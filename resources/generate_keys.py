import secrets
import string

def generate_secret_key(length=50):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    return ''.join(secrets.choice(chars) for _ in range(length))

# Generate 5 keys
print("Here are 5 secure Django SECRET_KEYs:\n")
for i in range(5):
    key = generate_secret_key()
    print(f"Option {i+1}: {key}\n")

print("\nChoose one and add it to your Render environment variables!")
