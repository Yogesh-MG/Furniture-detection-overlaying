import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from ultralytics import YOLO
import time

# Load the model
model_path = os.path.join(settings.BASE_DIR, 'image_segmentation/models/final_model.pt')
model = YOLO(model_path)

# Function to apply colored masks (you already have this function, but let's tweak it to match the color choice)
def apply_colored_masks(image, result, selected_color):
    # Define the color mapping based on user selection
    class_colors = {
        'red': [255, 0, 0],  # Red for class 0
        'green': [0, 255, 0],  # Green for class 1
        'blue': [0, 0, 255],  # Blue for class 2
    }
    color = class_colors[selected_color]
    
    mask_overlay = np.zeros_like(image)
    for mask, class_id in zip(result.masks.xy, result.boxes.cls):
        mask_resized = cv2.resize(mask, (image.shape[1], image.shape[0]))
        mask_overlay[mask_resized > 0.5] = color
        
    result_image = np.where(mask_overlay == 0, image, mask_overlay)
    return result_image

def show_prediction_with_colored_masks(image_path, selected_color):
    result = model.predict(source=image_path, conf=0.75, iou=0.1)
    img = mpimg.imread(image_path)

    # Apply the chosen color mask
    result_image = apply_colored_masks(img, result[0], selected_color)
    
    # Save the result image to a static folder
    output_path = os.path.join(settings.MEDIA_ROOT, 'output.jpg')
    plt.imshow(result_image)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    
    return output_path

# View to handle the form submission
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            selected_color = form.cleaned_data['color']

            # Save the uploaded image
            fs = FileSystemStorage()
            filename = fs.save(uploaded_image.name, uploaded_image)
            uploaded_image_url = fs.url(filename)
            

            # Get the file path of the uploaded image
            uploaded_image_path = os.path.join(settings.MEDIA_ROOT, filename)

            # Perform prediction and save the result
            result_image_path = show_prediction_with_colored_masks(uploaded_image_path, selected_color)
                  

            # Generate the result image URL
            result_image_url = os.path.join(settings.MEDIA_URL, 'output.jpg')
          

            # Pass both URLs to the template
            return render(request, 'index.html', {
                'form': form,
                'uploaded_image_url': uploaded_image_url,
                'result_image_url': result_image_url
            })

    else:
        form = ImageUploadForm()

    return render(request, 'index.html', {'form': form})

