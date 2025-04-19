import os
import cv2
import pickle
from keras_facenet import FaceNet

# Initialize FaceNet model once
model = FaceNet()

# Function to extract face embeddings
def extract_face_embedding(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    
    # Extract face embeddings
    embeddings = model.embeddings([image])
    return embeddings[0]

# Function to save embeddings with labels
def save_embeddings(dataset_folder, embeddings_file='embeddings.pkl'):
    embeddings_dict = {}

    # Loop through person folders
    for person_name in os.listdir(dataset_folder):
        person_folder_path = os.path.join(dataset_folder, person_name)
        
        if os.path.isdir(person_folder_path):  # Ensure it's a folder
            # Loop through images inside the person's folder
            for filename in os.listdir(person_folder_path):
                image_file_path = os.path.join(person_folder_path, filename)

                if image_file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    embedding = extract_face_embedding(image_file_path)
                    embeddings_dict[filename] = {'name': person_name, 'embedding': embedding}
    
    # Save embeddings dictionary
    with open(embeddings_file, 'wb') as f:
        pickle.dump(embeddings_dict, f)

    print(f"Embeddings saved to {embeddings_file}")

# Example usage
if __name__ == "__main__":
    dataset_folder_path = r"C:\Users\taufi\OneDrive\Desktop\Blockchain\VoterDAtabase\FaceDataset"
    save_embeddings(dataset_folder_path)
