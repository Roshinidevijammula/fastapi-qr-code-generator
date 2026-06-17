import os
import io
import uuid
import boto3
import qrcode
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

app = Flask(__name__)

# AWS S3 Configurations
S3_BUCKET = os.getenv("S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    if not data or "url" not in data or not data["url"].strip():
        return jsonify({"error": "URL is required"}), 400
    
    url = data["url"].strip()
    
    try:
        # Generate the QR Code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Save image to a BytesIO object
        img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        # Generate a unique key for the S3 object
        filename = f"qrcodes/{uuid.uuid4()}.png"
        
        # Attempt public-read ACL, fallback if S3 blocks ACLs
        try:
            s3_client.upload_fileobj(
                img_buffer,
                S3_BUCKET,
                filename,
                ExtraArgs={
                    "ContentType": "image/png",
                    "ACL": "public-read"
                }
            )
        except Exception as upload_err:
            print(f"ACL upload failed, trying standard upload: {upload_err}")
            # Re-create the buffer since upload_fileobj closes it on failure
            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            s3_client.upload_fileobj(
                img_buffer,
                S3_BUCKET,
                filename,
                ExtraArgs={
                    "ContentType": "image/png"
                }
            )
        
        # Construct public URL
        qr_url = f"https://{S3_BUCKET}.s3.{AWS_DEFAULT_REGION}.amazonaws.com/{filename}"
        
        return jsonify({"qr_url": qr_url})
        
    except Exception as e:
        print(f"Error generating or uploading QR code: {e}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
