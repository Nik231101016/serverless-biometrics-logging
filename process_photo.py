import json
import os
import sys
import boto3

# Initialize AWS Client SDKs using GitHub Environment Secrets
AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

s3_client = boto3.client("s3", region_name=AWS_REGION)
rekognition = boto3.client("rekognition", region_name=AWS_REGION)

def process_latest_employee_photo():
    if not BUCKET_NAME:
        print("🛑 Error: S3_BUCKET_NAME environment variable is missing.")
        sys.exit(1)

    # Search project workspace directory for image files
    valid_extensions = (".jpg", ".jpeg", ".png")
    photo_files = [f for f in os.listdir(".") if f.lower().endswith(valid_extensions)]

    if not photo_files:
        print("📁 Inspection Notice: No new employee photo detected in current workspace commit.")
        return

    # Sort to pick the most recent image uploaded
    target_photo = photo_files[0]
    s3_key = f"employees/{target_photo}"

    print(f"📸 Found photo targeting processing loop: {target_photo}")
    print(f"📤 Uploading {target_photo} securely to Amazon S3 bucket...")
    
    # 1. Upload photo to S3
    with open(target_photo, "rb") as image_file:
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=image_file,
            ContentType="image/jpeg"
        )
    print("🟢 S3 Storage Archival Complete.")

    # 2. Trigger Amazon Rekognition Face Detection API
    print("🧠 Triggering Amazon Rekognition computer vision models...")
    response = rekognition.detect_faces(
        Image={"S3Object": {"Bucket": BUCKET_NAME, "Name": s3_key}},
        Attributes=["DEFAULT"]
    )

    face_details = response.get("FaceDetails", [])
    num_faces = len(face_details)

    print("\n========= REKOGNITION BIOMETRIC REPORT =========")
    print(f"Number of Faces Detected : {num_faces}")
    
    faces_summary = []
    for index, face in enumerate(face_details, start=1):
        confidence = round(face["Confidence"], 2)
        print(f"👤 Face #{index} Confidence Threshold : {confidence}%")
        faces_summary.append({
            "face_index": index,
            "confidence": confidence
        })
    print("================================================\n")

    # 3. Save Compiled Diagnostics as result.json
    output_payload = {
        "processed_file": target_photo,
        "s3_storage_uri": f"s3://{BUCKET_NAME}/{s3_key}",
        "total_faces_detected": num_faces,
        "faces": faces_summary
    }

    with open("result.json", "w") as json_out:
        json.dump(output_payload, json_out, indent=4)
        
    print("💾 Compiled analytics metrics written out safely to result.json.")

if __name__ == "__main__":
    process_latest_employee_photo()
