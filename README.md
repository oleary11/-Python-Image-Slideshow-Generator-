Description: A Python script for creating a slideshow video from images in two directories. The script supports various image types, handles image processing tasks, and uses FFmpeg with NVENC for video encoding. The output is a slideshow video in mp4 format.

README:

# Python Image Slideshow Generator

This Python script creates a slideshow video from images residing in two directories. It supports image types including png, jpg, jpeg, bmp, gif, heic, and heif, and uses FFmpeg with NVENC for video encoding. The output video is named 'slideshow.mp4'.

## Functions

The script defines several functions:

- `get_images_from_dir(directory)`: Retrieves all image files from a specified directory.
- `resize_and_center_image(img, canvas_size=(1920, 1080))`: Resizes an image to fit within a given canvas size while maintaining aspect ratio, and places it at the center of a black background.
- `load_and_process_images(image_paths, canvas_size=(1920, 1080))`: Retrieves images from given paths, corrects their orientation, and fits them onto a black canvas.
- `create_temp_images(image_paths, duration, fps)`: Creates temporary images and a list file for FFmpeg.
- `cleanup_temp_files(temp_images)`: Removes temporary images and the FFmpeg input list.

## Usage

To use this script, simply run it in your Python environment, ensuring that the directories containing your images are correctly specified.

## Dependencies

This script requires the following Python modules: PIL, FFmpeg-python, and others that handle logging and HEIC image support. Please ensure these are installed before running the script.

## Disclaimer

This script is intended for personal use and might not meet professional video production standards. Always back up your original image files before processing.