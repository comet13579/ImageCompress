from PIL import Image
import time
import sys
import os

class ImageCompressor:
    def __init__(self, image_paths:list, quality=85, openfolder=False, output_format="jpg"):
        self.image_paths = image_paths
        self.quality = quality
        self.output_paths = []
        self.output_folder = set()
        self.openfolder = openfolder
        self.output_format = output_format
        self._generate_output_path()
    
    def _generate_output_path(self):
        for image_path in self.image_paths:
            file_name, originalext= os.path.splitext(image_path)
            print(f"{file_name}_compressed.")
            self.output_paths.append(f"{file_name}_compressed{self.quality}.{self.output_format}")
            self.output_folder.add(os.path.dirname(image_path) or '.')
    
    def compress_single(self, image_path:str, output_path:str):
        try:
            if self.output_format.upper() == 'JPG':
                self.output_format = 'JPEG'
            with Image.open(image_path) as img:
                img = img.convert('RGB')
                img.save(output_path, self.output_format.upper(), quality=self.quality)
            print(f"Compressed image saved as: {output_path} to {os.path.getsize(output_path) // 1024} KB")
        except Exception as e:
            print(f"Error compressing {image_path}: {str(e)}")

    def compress(self, progress_callback=None):
        inittime = time.time()
        for i in range(len(self.image_paths)):
            self.compress_single(self.image_paths[i], self.output_paths[i])
            if progress_callback:
                progress_callback(i + 1)
                
        # Open all parent folders after compression
        if self.openfolder:
            for folder in self.output_folder:
                abs_folder = os.path.abspath(folder)
                print(f"Opening folder: {abs_folder}")
                if sys.platform.startswith('darwin'):  # macOS
                    os.system(f"open '{abs_folder}'")
                elif sys.platform.startswith('win'):  # Windows
                    os.system(f'explorer "{abs_folder}"')  # Use double quotes for Windows
                elif sys.platform.startswith('linux'):  # Linux
                    os.system(f"xdg-open '{abs_folder}'")

        return time.time() - inittime

if __name__ == "__main__":  
    compressor = ImageCompressor(["test.jpg"], 85)
    compressor.compress()
