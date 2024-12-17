import os
import logging
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

# Register HEIC support
register_heif_opener()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def get_images_from_dir(directory):
    """Load all image files from a directory."""
    supported_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.heic', '.heif')
    return sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(supported_extensions)])

def resize_and_center_image(img, canvas_size=(1920, 1080)):
    """Resize the image to fit within the canvas while maintaining its aspect ratio."""
    canvas = Image.new("RGB", canvas_size, (0, 0, 0))  # Black background
    img.thumbnail(canvas_size, Image.LANCZOS)  # Resize while maintaining aspect ratio
    x_offset = (canvas_size[0] - img.width) // 2
    y_offset = (canvas_size[1] - img.height) // 2
    canvas.paste(img, (x_offset, y_offset))
    return canvas

def load_and_process_images(image_paths, canvas_size=(1920, 1080)):
    """Load images, correct their orientation, and fit them on a black canvas."""
    processed_images = []
    for i, path in enumerate(image_paths, start=1):
        logging.info(f"Processing image {i}/{len(image_paths)}: {path}")
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)  # Correct orientation
        img = resize_and_center_image(img, canvas_size)  # Center on black background
        processed_images.append(img)
    return processed_images

def create_temp_images(image_paths, duration, fps):
    """Create temporary images and a list file for FFmpeg."""
    temp_images = [f"temp_{i:04d}.png" for i in range(len(image_paths))]
    with open("image_list.txt", "w") as f:
        for i, (path, img) in enumerate(zip(temp_images, image_paths), start=1):
            logging.info(f"Saving temp image {i}/{len(image_paths)}")
            img.save(path)
            f.write(f"file '{path}'\n")
            f.write(f"duration {duration}\n")
        f.write(f"file '{temp_images[-1]}'\n")
        f.write("duration 0.1\n")  # Short final frame to avoid lingering
    return temp_images

def cleanup_temp_files(temp_images):
    """Remove temp images and FFmpeg input list."""
    logging.info("Cleaning up temporary files...")
    for path in temp_images:
        if os.path.exists(path):
            os.remove(path)
    if os.path.exists("image_list.txt"):
        os.remove("image_list.txt")
    logging.info("Temporary files cleaned up.")

def main():
    dir1 = os.path.join(os.getcwd(), "Person 1")
    dir2 = os.path.join(os.getcwd(), "Person 2")
    output_file = "slideshow.mp4"
    duration_per_image = 6  # seconds
    fps = 60

    # Get images from directories
    images_dir1 = get_images_from_dir(dir1)
    images_dir2 = get_images_from_dir(dir2)

    # Alternate images from directories
    combined_images = []
    for img1, img2 in zip(images_dir1, images_dir2):
        combined_images.append(img1)
        combined_images.append(img2)
    combined_images += images_dir1[len(images_dir2):]
    combined_images += images_dir2[len(images_dir1):]

    # Process images and prepare for FFmpeg
    logging.info("Loading and processing images...")
    processed_images = load_and_process_images(combined_images)
    logging.info("Creating temp images and FFmpeg input list...")
    temp_images = create_temp_images(processed_images, duration_per_image, fps)

    # Use FFmpeg with NVENC to encode the video
    logging.info("Starting video encoding with FFmpeg and NVIDIA NVENC...")
    os.system(
        f"ffmpeg -y -f concat -safe 0 -i image_list.txt -vf \"fps={fps},format=yuv420p\" -c:v h264_nvenc -preset fast {output_file}"
    )
    logging.info("Video encoding complete!")

    # Clean up temporary files
    cleanup_temp_files(temp_images)

if __name__ == "__main__":
    main()
