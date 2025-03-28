import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

# Load the trained model
MODEL_PATH = os.path.join("artifacts", "training", "model.h5")
model = load_model(MODEL_PATH)

# Define class labels
CLASS_LABELS = [
    "Adenocarcinoma (Left Lower Lobe)",
    "Large Cell Carcinoma (Left Hilum)",
    "Normal",
    "Squamous Cell Carcinoma (Left Hilum)"
]

# Function to predict image
def predict_image(img):
    img = img.resize((224, 224))  # Resize image to match model input
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)  # Expand dimensions to match model input
    img = img / 255.0  # Normalize
    
    predictions = model.predict(img)
    
    # If model outputs probabilities (sigmoid)
    if predictions.shape[1] == 1:
        result = int(predictions[0][0] > 0.5)
    else:
        result = np.argmax(predictions, axis=1)[0]
    
    return CLASS_LABELS[result]

# Streamlit UI
st.set_page_config(page_title="Chest Cancer Prediction", layout="centered")

st.title("🩺 Chest Cancer Detection")
st.write("Upload a chest X-ray image to predict the type of Chest cancer.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    # Load image
    img = image.load_img(uploaded_file, target_size=(224, 224))

    # Predict button
    if st.button("Predict"):
        prediction = predict_image(img)
        st.success(f"🩻 **Prediction:** {prediction}")
