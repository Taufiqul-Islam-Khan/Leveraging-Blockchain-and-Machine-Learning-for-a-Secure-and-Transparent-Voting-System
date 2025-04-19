# import os
# import cv2
# import pickle
# from sklearn.metrics.pairwise import cosine_similarity
# from keras_facenet import FaceNet

# # Initialize FaceNet model once
# model = FaceNet()

# # Function to extract face embeddings using FaceNet
# def extract_face_embedding(image_path):
#     # Load the image
#     image = cv2.imread(image_path)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    
#     # Extract face embeddings
#     embeddings = model.embeddings([image])
#     return embeddings[0]

# # Function to check if the new image is the same person (even with different angle)
# def is_same_person(new_image_path, embeddings_file='embeddings.pkl', threshold=0.7):
#     # Load precomputed embeddings
#     with open(embeddings_file, 'rb') as f:
#         embeddings_dict = pickle.load(f)

#     # Extract the embedding for the new image
#     new_image_embedding = extract_face_embedding(new_image_path)
    
#     # Compare the new image embedding with precomputed embeddings
#     for filename, data in embeddings_dict.items():
#         stored_embedding = data['embedding']  # Extract only the embedding
        
#         # Compute the cosine similarity
#         similarity = cosine_similarity([new_image_embedding], [stored_embedding])[0][0]
        
#         # If similarity is above the threshold, it's likely the same person
#         if similarity >= threshold:
#             print(f"Match found! Image '{filename}' belongs to {data['name']}.")
#             return True  # Match found
    
#     print("No match found.")
#     return False  # No match

# # Example usage
# if __name__ == "__main__":
#     new_image_path = r"C:\Users\taufi\OneDrive\Desktop\Blockchain\VoterDAtabase\VoterImages\Taufiq.jpg"
#     embeddings_file = r"embeddings.pkl"  # Path to the saved embeddings file
    
#     # Check if the new image matches any image in the folder
#     is_same_person(new_image_path, embeddings_file)

import os
import cv2
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from keras_facenet import FaceNet

# Initialize FaceNet model once
model = FaceNet()

# Function to extract face embeddings using FaceNet
def extract_face_embedding(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    
    # Extract face embeddings
    embeddings = model.embeddings([image])
    return embeddings[0]

# Function to check if the new image is the same person (even with different angles)
def is_same_person(new_image_path, embeddings_file='embeddings.pkl', threshold=0.5):
    # Load precomputed embeddings
    with open(embeddings_file, 'rb') as f:
        embeddings_dict = pickle.load(f)

    # Extract the embedding for the new image
    new_image_embedding = extract_face_embedding(new_image_path)
    
    # Compare the new image embedding with precomputed embeddings
    for filename, data in embeddings_dict.items():
        stored_embedding = data['embedding']  # Extract only the embedding
        
        # Compute the cosine similarity
        similarity = cosine_similarity([new_image_embedding], [stored_embedding])[0][0]
        
        # If similarity is above the threshold, it's likely the same person
        if similarity >= threshold:
            print(f"Match found! Image '{filename}' belongs to {data['name']}.")
            return data['name']  # Match found
    
    print("No match found.")
    return False  # No match

# Function to capture an image from the webcam
def capture_image(save_path='captured_image.jpg'):
    cap = cv2.VideoCapture(0)  # Open the webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None

    print("Press 'SPACE' to capture the image. Press 'ESC' to exit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        cv2.imshow("Capture Image", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # SPACE key to capture
            cv2.imwrite(save_path, frame)
            print(f"Image captured and saved as {save_path}")
            break
        elif key == 27:  # ESC key to exit
            print("Image capture canceled.")
            save_path = None
            break

    cap.release()
    cv2.destroyAllWindows()
    return save_path

# # Main Execution
# if __name__ == "__main__":
#     choice = input("Do you want to capture an image? (yes/no): ").strip().lower()

#     if choice == 'yes':
#         new_image_path = capture_image()
#         if new_image_path:
#             is_same_person(new_image_path)
#     else:
#         new_image_path = input("Enter the path of the image to check: ").strip()
#         is_same_person(new_image_path)
