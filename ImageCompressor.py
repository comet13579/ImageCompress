from PIL import Image
import threading
import time
import sys
import os

class ImageCompressor:
    def __init__(self, image_paths, quality):
        self.image_paths = image_paths
        self.quality = quality
        self.output_paths = []
        self._generate_output_path()
    
    def _generate_output_path(self):
        for image_path in self.image_paths:
            file_name, originalext= os.path.splitext(image_path)
            print(f"{file_name}_compressed.")
            self.output_paths.append(f"{file_name}_compressed{self.quality}.jpg")
    
    def compress_single(self, image_path, output_path):
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
        return time.time() - inittime

if __name__ == "__main__":  
    compressor = ImageCompressor(["14.5k.png"], 10)
    compressor.compress()


