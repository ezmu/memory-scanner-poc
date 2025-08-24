import numpy as np
import random
import re
import os
import requests
from PIL import Image
from io import BytesIO

# ========================
# 1 Allocate 50 MB heap
# ========================
total_size_bytes = 50 * 1024 * 1024
heap_block = np.zeros(total_size_bytes, dtype=np.uint8)  # Initialize to zeros

# ========================
# 2 Define 10 MB scan range
# ========================
scan_start = 5 * 1024 * 1024       # Start of 10MB scan range
scan_size = 10 * 1024 * 1024
scan_end = scan_start + scan_size

# ========================
# 3 Define target data
# ========================
target_words = [
    "SecretKey123", "password", "API_KEY", "token", "DataBlock", "AdminPass", "SessionID",
    "EncryptionKey", "UserToken", "AuthCode", "PrivateKey", "BackupKey", "RootAccess",
    "MasterPassword", "CryptoKey", "LoginToken", "SecureString", "SecretPhrase", "DBPassword",
    "AccessToken", "Key1234", "PrivateData", "HiddenValue", "SecretValue"
]

other_texts = [
    "Hello world!", "Python rocks!", "Test sequence", "Random text here", 
    "Sample data block", "Temporary string", "Debugging memory", 
    "Memory scanning example", "https://example.com", "http://test.local"
]

# URLs for real images
image_urls = [
    "https://picsum.photos/200/300",
    "https://picsum.photos/200/300?grayscale",
    "https://picsum.photos/200/300?blur=5"
]

# ========================
# 4 Inject words and texts into memory
# ========================
offset = scan_start
for word in target_words + other_texts:
    bytes_text = word.encode()
    if offset + len(bytes_text) < scan_end:
        heap_block[offset:offset+len(bytes_text)] = np.frombuffer(bytes_text, dtype=np.uint8)
        offset += len(bytes_text) + random.randint(50, 200)  # small gap

# ========================
# 5 Download and inject images
# ========================
for idx, url in enumerate(image_urls):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_data = img_byte_arr.getvalue()
    if offset + len(img_data) < scan_end:
        heap_block[offset:offset+len(img_data)] = np.frombuffer(img_data, dtype=np.uint8)
        offset += len(img_data) + 50

# ========================
# 6️ Helper functions
# ========================
def byte_to_char(b):
    if isinstance(b, np.ndarray):
        return ''.join(chr(x) if 32 <= x <= 126 else ' ' for x in b)
    return chr(b) if 32 <= b <= 126 else ' '

url_pattern = re.compile(r'https?://[^\s]+')
os.makedirs("extracted_images", exist_ok=True)

# ========================
# 7 Scan memory
# ========================
min_length = 6
i = scan_start
found_words = set()

print(f"Scanning memory from offset {scan_start} to {scan_end} (10MB)")

while i < scan_end - 8:
    # Gather printable sequence
    sequence = ''
    j = i
    while j < scan_end and 32 <= heap_block[j] <= 126:
        sequence += chr(heap_block[j])
        j += 1

    if len(sequence) >= min_length:
        # Extract URLs
        urls = url_pattern.findall(sequence)
        for url in urls:
            print(f"[URL] {url}")

        # Extract target words with context
        for word in target_words:
            start_idx = 0
            while True:
                found_idx = sequence.find(word, start_idx)
                if found_idx == -1:
                    break
                abs_start = i + found_idx
                abs_end = abs_start + len(word)

                # Skip if word already found
                if (word, abs_start) in found_words:
                    start_idx = found_idx + len(word)
                    continue

                found_words.add((word, abs_start))

                # First readable sequence before
                k = abs_start - 1
                before_seq = ''
                while k >= scan_start:
                    b = heap_block[k]
                    if 32 <= b <= 126:
                        before_seq = chr(b) + before_seq
                        k -= 1
                    elif before_seq:
                        break
                    else:
                        k -= 1

                # First readable sequence after
                k = abs_end
                after_seq = ''
                while k < scan_end:
                    b = heap_block[k]
                    if 32 <= b <= 126:
                        after_seq += chr(b)
                        k += 1
                    elif after_seq:
                        break
                    else:
                        k += 1

                print(f"[WORD] {before_seq} {word} {after_seq}".strip())
                start_idx = found_idx + len(word)

        i = j
    else:
        # ------------------------
        # Extract images (JPEG)
        if heap_block[i] == 0xFF and heap_block[i+1] == 0xD8:
            start = i
            for j_img in range(i+2, scan_end-1):
                if heap_block[j_img] == 0xFF and heap_block[j_img+1] == 0xD9:
                    end = j_img+2
                    filename = f"extracted_images/image_{start}.jpg"
                    with open(filename, "wb") as f:
                        f.write(heap_block[start:end].tobytes())
                    print(f"[JPEG extracted] offset {start}-{end} -> {filename}")
                    i = end
                    break
        else:
            i += 1
