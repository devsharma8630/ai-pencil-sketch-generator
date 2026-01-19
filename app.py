from flask import Flask, render_template_string, request
import cv2, os
from cartoon import cartoonize

app = Flask(__name__)
UPLOAD_FOLDER = "static"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title> AI Cartoon Converter</title>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 30px;
    padding: 50px;
    max-width: 1200px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

h1 {
    text-align: center;
    color: #667eea;
    font-size: 3em;
    margin-bottom: 15px;
    font-weight: 700;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.2em;
    margin-bottom: 40px;
}

.upload-section {
    text-align: center;
    margin-bottom: 40px;
}

.file-input-wrapper {
    position: relative;
    display: inline-block;
    cursor: pointer;
    margin-bottom: 20px;
}

.file-input-wrapper input[type="file"] {
    position: absolute;
    left: -9999px;
}

.file-input-label {
    display: inline-block;
    padding: 20px 50px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50px;
    cursor: pointer;
    font-size: 1.2em;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.file-input-label:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
}

.file-name {
    display: block;
    margin-top: 15px;
    color: #666;
    font-size: 0.95em;
}

.convert-btn {
    padding: 18px 60px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border: none;
    border-radius: 50px;
    font-size: 1.3em;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(245, 87, 108, 0.4);
    margin-top: 20px;
}

.convert-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(245, 87, 108, 0.6);
}

.convert-btn:active {
    transform: translateY(-1px);
}

.results {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    margin-top: 50px;
}

.image-card {
    background: white;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.image-card:hover {
    transform: translateY(-5px);
}

.image-card h3 {
    color: #667eea;
    margin-bottom: 20px;
    font-size: 1.5em;
    text-align: center;
}

.image-card img {
    width: 100%;
    max-width: 100%;
    height: auto;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.download-btn {
    display: inline-block;
    padding: 15px 40px;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    text-decoration: none;
    border-radius: 50px;
    margin-top: 30px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(79, 172, 254, 0.4);
}

.download-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(79, 172, 254, 0.6);
}

.features {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    margin: 50px 0;
    text-align: center;
}

.feature {
    padding: 25px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border-radius: 20px;
    transition: all 0.3s ease;
}

.feature:hover {
    transform: translateY(-5px);
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
}

.feature-icon {
    font-size: 3em;
    margin-bottom: 15px;
}

.feature h4 {
    color: #667eea;
    margin-bottom: 10px;
    font-size: 1.2em;
}

.feature p {
    color: #666;
    font-size: 0.95em;
}

.loader {
    display: none;
    margin: 30px auto;
    border: 8px solid #f3f3f3;
    border-top: 8px solid #667eea;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
    .results {
        grid-template-columns: 1fr;
    }
    
    .features {
        grid-template-columns: 1fr;
    }
    
    .container {
        padding: 30px 20px;
    }
    
    h1 {
        font-size: 2em;
    }
}
</style>
</head>
<body>
<div class="container">
    <h1>Sketch Converter AI</h1>
    
    <p class="subtitle">Transform your photos into beautiful pencil sketches</p>
    
    {% if not uploaded %}
    <div class="features">
        <div class="feature">
            <div class="feature-icon"></div>
            <h4>AI-Powered</h4>
            <p>Advanced algorithms create stunning sketches</p>
        </div>
        <div class="feature">
            <div class="feature-icon"></div>
            <h4>Super Fast</h4>
            <p>Your sketch will be ready in few seconds</p>
        </div>
        <div class="feature">
            <div class="feature-icon"></div>
            <h4>High Quality</h4>
            <p>Professional-grade results every time</p>
        </div>
    </div>
    {% endif %}
    
    <div class="upload-section">
        <form method="POST" enctype="multipart/form-data" id="uploadForm">
            <div class="file-input-wrapper">
                <input type="file" name="photo" id="fileInput" accept="image/*" required>
                <label for="fileInput" class="file-input-label">
                    📸 Choose Your Photo
                </label>
            </div>
            <div class="file-name" id="fileName"></div>
            <div class="loader" id="loader"></div>
            <button type="submit" class="convert-btn">Convert to Sketch</button>
        </form>
    </div>
    
    {% if uploaded %}
    <div class="results">
        <div class="image-card">
            <h3> Original Image</h3>
            <img src="{{uploaded}}" alt="Original">
        </div>
        <div class="image-card">
            <h3>✨ Sketch Image</h3>
            <img src="{{cartoon}}" alt="Cartoon">
            <div style="text-align: center;">
                <a href="{{cartoon}}" download="cartoon_sketch.jpg" class="download-btn">
                    ⬇️ Download Image
                </a>
            </div>
        </div>
    </div>
    {% endif %}
</div>

<script>
document.getElementById('fileInput').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name;
    document.getElementById('fileName').textContent = fileName ? `Selected: ${fileName}` : '';
});

document.getElementById('uploadForm').addEventListener('submit', function() {
    document.getElementById('loader').style.display = 'block';
});
</script>
</body>
</html>
'''

@app.route("/", methods=["GET","POST"])
def home():
    uploaded = None
    cartoon_img = None
    if request.method == "POST":
        file = request.files['photo']
        up_path = os.path.join(UPLOAD_FOLDER,"upload.jpg")
        file.save(up_path)
        cartoon = cartoonize(up_path)
        out_path = os.path.join(UPLOAD_FOLDER,"cartoon.jpg")
        cv2.imwrite(out_path, cartoon)
        uploaded = up_path
        cartoon_img = out_path
    return render_template_string(HTML, uploaded=uploaded, cartoon=cartoon_img)

if __name__ == "__main__":

    if __name__ == "__main__":
         app.run(host="0.0.0.0", port=10000)
