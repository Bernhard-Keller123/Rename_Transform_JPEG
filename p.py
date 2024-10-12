import os
from PIL import Image
import streamlit as st
import io

# Function to convert and prepare images for download
def convert_and_prepare_images(file_paths):
    converted_images = []

    for idx, uploaded_file in enumerate(file_paths, start=1):
        try:
            # Open the image
            img = Image.open(uploaded_file)
            width, height = img.size
            rotated = False

            # Check if the image is in portrait mode (height > width)
            if height > width:
                # Rotate the image 90 degrees to make it landscape
                img = img.rotate(90, expand=True)
                rotated = True
                st.info(f"Image {uploaded_file.name} was rotated to landscape.")
            else:
                st.info(f"Image {uploaded_file.name} is already in landscape.")

            # Convert the image to RGB
            rgb_img = img.convert('RGB')

            # Save the image to a BytesIO object instead of a file
            img_bytes = io.BytesIO()
            rgb_img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)  # Reset the pointer to the start of the BytesIO object

            # Append the in-memory image and its name for download
            converted_images.append((img_bytes, f"Image_{idx:03d}.jpg"))

        except Exception as e:
            st.error(f"Error processing image {uploaded_file.name}: {e}")

    return converted_images

def main():
    st.title("Image Dropper and Converter")

    # File uploader for multiple image files
    uploaded_files = st.file_uploader("Drag and drop images here or click to upload.", type=["jpg", "png"], accept_multiple_files=True)

    if uploaded_files:
        st.write(f"{len(uploaded_files)} image(s) uploaded.")

        # Display uploaded images
        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file)
            st.image(img, caption=f"Original Image: {uploaded_file.name}", use_column_width=True)

        # Button to convert and download images
        if st.button("Convert and Prepare for Download"):
            converted_images = convert_and_prepare_images(uploaded_files)

            # Display download links for each converted image
            for img_bytes, filename in converted_images:
                st.download_button(
                    label=f"Download {filename}",
                    data=img_bytes,
                    file_name=filename,
                    mime="image/jpeg"
                )

if __name__ == "__main__":
    main()
