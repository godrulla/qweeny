# AI Image Generator App

A simple Flask web application for generating images using Stable Diffusion models from Hugging Face.

## 🎯 Features

- **Text-to-Image Generation**: Generate high-quality images from text prompts
- **Lightweight Model**: Uses Stable Diffusion 1.5 (~4GB download)
- **Multiple Aspect Ratios**: Choose from various aspect ratios (16:9, 1:1, 9:16, etc.)
- **Web Interface**: Easy-to-use web interface with example prompts
- **Image Download**: Download generated images directly
- **Local Operation**: Runs completely offline after initial model download

## 🚀 Quick Start

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the app:**
```bash
./run.sh
```
*Or manually: `source venv/bin/activate && python3 app.py`*

4. **First Run**: Model will download (~4GB) - takes 5-15 minutes
5. **Access**: Open `http://localhost:5000` in browser

## 📋 System Requirements

- Python 3.8+
- 4GB+ free disk space (for model)
- 8GB+ RAM recommended
- CPU or GPU (GPU faster but not required)

## 🖼️ Image Generation

- **Resolution**: Optimized 512px base (perfect for SD 1.5)
- **Speed**: ~30s on GPU, ~2-5min on CPU
- **Quality**: High-quality artistic images
- **Storage**: Images saved in `static/generated/`

## 💡 Example Prompts

- "A majestic mountain landscape at sunrise"
- "Cyberpunk city with neon lights"
- "Portrait of a wise old wizard"
- "Cute robot in a garden"

## 🛠️ Troubleshooting

**Virtual Environment Issues:**
- Use `python3 -m venv venv` if getting "externally managed" errors

**Slow Generation:**
- First generation is slower (model loading)
- CPU generation takes 2-5 minutes
- Consider reducing image size for faster results

**Model Download:**
- Requires stable internet for initial ~4GB download
- Model cached locally after first download