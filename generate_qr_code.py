import json
import os
import qrcode
import os

def generate_qr_code(user_id, name):
    qr_folder = 'static/qr_codes'
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)  # Create the folder if it doesn't exist

    data = {
        "user_id": user_id,
        "name": name
    }

    json_data = json.dumps(data)  # Convert to JSON string

    print("Encoded QR Data:", json_data)  # 🔹 Debugging: Print JSON before saving
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(json_data)  # ✅ Storing JSON string inside QR code
    qr.make(fit=True)

    qr_image = qr.make_image(fill='black', back_color='white')
    
    qr_path = f"static/qr_codes/{user_id}_voting_qr.png"
    qr_image.save(qr_path)

    print(f"QR code saved for user {user_id}")
    return qr_path

