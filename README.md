Memory Scanner PoC
==================

Short Description:
-----------------
Proof of Concept for scanning memory to extract readable text, URLs, and images from allocated memory blocks.

Detailed Description:
---------------------
This repository contains a Proof of Concept demonstrating how memory can be scanned programmatically to uncover:

- Readable text (ASCII strings)
- URLs embedded in memory
- Images stored in memory (JPEG format)

⚠️ Disclaimer: This is an educational project to illustrate memory analysis techniques. 
Do not run on production or sensitive systems. Use only synthetic/test data.

Features:
---------
- Allocate a memory block and inject sample text, URLs, and images.
- Scan memory sequentially to find readable strings.
- Extract context before and after target words.
- Detect and extract images by identifying JPEG headers and footers.
- Output results in a human-readable format.

Requirements:
-------------
- Python 3.x
- Libraries:
  - numpy
  - requests
  - Pillow
  - langdetect
  - re

Usage:
------
1. Clone the repository:
   git clone https://github.com/username/memory-scanner-poc.git
   cd memory-scanner-poc

2. Install dependencies:
   pip install -r requirements.txt

3. Run the script:
   python memory_scanner.py

4. Review the output:
   - Found readable text sequences
   - Extracted URLs
   - Saved images (JPEG) from memory

Learning Objectives:
-------------------
- Understanding how memory stores temporary data.
- How readable text and images can reside in RAM.
- The importance of proper data handling and memory cleanup for security.

Tip:
----
Use only test or synthetic data. Never attempt to scan memory containing sensitive or production data.

Author Information
------------------
Name: Ez Eldeen Mushtaha
Email: ezmu@example.com
LinkedIn: https://www.linkedin.com/in/ezmush/
