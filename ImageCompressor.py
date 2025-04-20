from PIL import Image
import threading
import time
import sys
import os

class ImageCompressor:
    def __init__(self, image_paths:list, quality=85, openfolder=False):
        self.image_paths = image_paths
        self.quality = quality
        self.output_paths = []
        self.output_folder = set()
        self.openfolder = openfolder
        self._generate_output_path()
    
    def _generate_output_path(self):
        for image_path in self.image_paths:
            file_name, originalext= os.path.splitext(image_path)
            print(f"{file_name}_compressed.")
            self.output_paths.append(f"{file_name}_compressed{self.quality}.jpg")
            self.output_folder.add(os.path.dirname(image_path) or '.')
    
    def compress_single(self, image_path:str, output_path:str):
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            img.save(output_path, "JPEG", quality=self.quality)
        print(f"Compressed image saved as: {output_path} to {os.path.getsize(output_path) // 1024} KB")

    def compress(self):
        inittime = time.time()
        threads = []
        for i in range(len(self.image_paths)):
            thread = threading.Thread(
                target=self.compress_single,
                args=(self.image_paths[i], self.output_paths[i])
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        # Open all parent folders after compression
        if self.openfolder:
            for folder in self.output_folder:
                if sys.platform.startswith('darwin'):  # macOS
                    os.system(f"open {folder}")
                elif sys.platform.startswith('win'):  # Windows
                    os.system(f"start {folder}")
                elif sys.platform.startswith('linux'):  # Linux
                    os.system(f"xdg-open {folder}")

        return time.time() - inittime

if __name__ == "__main__":  
    compressor = ImageCompressor(["test.jpg"], 85)
    compressor.compress()


