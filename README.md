# AI Pencil Sketch Generator

An AI-powered application that transforms real photos into realistic
hand-drawn pencil portraits on a white paper background.

This project focuses on **face preservation**, **background removal**, and
**artistic sketch generation** using computer vision techniques.

---

## Features
- Upload any photo
- Background removal (white canvas)
- Face-preserving pencil sketch
- Realistic hand-drawn look
- Download final image
- Simple web interface (Flask)

---

## Technologies Used
- Python
- OpenCV
- NumPy
- Flask

---

## How It Works
1. User uploads an image
2. Background is removed using GrabCut
3. Image is converted into pencil sketch
4. Sketch is rendered on white paper
5. User downloads the final output

---

## Run Locally

```bash
pip install -r requirements.txt
python app.py
