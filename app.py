from flask import Flask, request, render_template, jsonify, send_file
from diffusers import DiffusionPipeline
import torch
import os
from datetime import datetime
import uuid

app = Flask(__name__)

# Global variables
pipe = None
device = None
torch_dtype = None

def initialize_model():
    global pipe, device, torch_dtype
    
    # Use a much lighter model that's perfect for local use
    model_name = "runwayml/stable-diffusion-v1-5"  # ~4GB instead of 20GB+
    
    if torch.cuda.is_available():
        torch_dtype = torch.bfloat16
        device = "cuda"
    else:
        torch_dtype = torch.float32
        device = "cpu"
    
    print(f"Loading Stable Diffusion 1.5 model on {device}...")
    print("This is a lightweight model (~4GB) perfect for local use!")
    
    try:
        pipe = DiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch_dtype,
            use_safetensors=True
        )
        pipe = pipe.to(device)
        print("Model loaded successfully!")
        
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Trying alternative model...")
        
        # Even lighter fallback
        alt_model = "CompVis/stable-diffusion-v1-4"
        pipe = DiffusionPipeline.from_pretrained(
            alt_model,
            torch_dtype=torch_dtype
        )
        pipe = pipe.to(device)
        print("Alternative model loaded successfully!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        negative_prompt = data.get('negative_prompt', ' ')
        aspect_ratio = data.get('aspect_ratio', '16:9')
        language = data.get('language', 'en')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Magic prompts for quality enhancement
        positive_magic = {
            "en": "Ultra HD, 4K, cinematic composition.",
            "zh": "超清，4K，电影级构图"
        }
        
        # Aspect ratio configurations optimized for SD 1.5 (512px base)
        aspect_ratios = {
            "1:1": (512, 512),
            "16:9": (768, 448),
            "9:16": (448, 768),
            "4:3": (640, 512),
            "3:4": (512, 640),
            "3:2": (768, 512),
            "2:3": (512, 768),
        }
        
        width, height = aspect_ratios.get(aspect_ratio, aspect_ratios["16:9"])
        
        # Generate image
        enhanced_prompt = prompt + " " + positive_magic.get(language, positive_magic["en"])
        
        # Generate image using standard Stable Diffusion parameters
        image = pipe(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_inference_steps=50,
            guidance_scale=7.5,
            generator=torch.Generator(device=device).manual_seed(42)
        ).images[0]
        
        # Save image with unique filename
        filename = f"generated_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join('static', 'generated', filename)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        image.save(filepath)
        
        return jsonify({
            'success': True,
            'image_url': f'/static/generated/{filename}',
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_image(filename):
    filepath = os.path.join('static', 'generated', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/generated', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Initialize model
    initialize_model()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)