from PIL import Image
import sys
import os

class ImageCompressor:
    def __init__(self, image_paths, quality, format):
        self.image_paths = image_paths
        self.quality = quality
        self.format = format
        self.output_path = []
        self._generate_output_path()
    
    def _generate_output_path(self):
        for image_path in self.image_paths:
            file_name, originalext= os.path.splitext(image_path)
            print(f"{file_name}_compressed.{self.format}")
            self.output_path.append(f"{file_name}_compressed{self.quality}.{self.format}")
    
    def compress(self):
        for i in range(len(self.image_paths)):
            with Image.open(self.image_paths[i]) as img:
                img.save(self.output_path[i], self.format,quality=self.quality)
            print(f"Compressed image saved as: {self.output_path[i]} to {os.path.getsize(self.output_path[i]) // 1000} KB")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <image_path> <quality_percentage>")
        sys.exit(1)
    
    compressor = ImageCompressor(["DSC05951.png","DSC05952.png","WhatsApp Image 2021-05-24 at 16.22.29.jpeg"], int(sys.argv[2]),"PNG")
    compressor.compress()


