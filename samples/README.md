# Sample Images

This directory contains sample images for testing the background removal application.

## Usage

1. Run the application
2. Drag and drop images from this folder to the queue
3. Select output settings
4. Click "Start Processing"

## Sample Images

Due to licensing, sample images are not included in the repository. You can:

1. Add your own test images here
2. Download free stock photos from:
   - [Unsplash](https://unsplash.com)
   - [Pexels](https://pexels.com)
   - [Pixabay](https://pixabay.com)

## Recommended Test Cases

- **Products**: Items with clear edges (phones, bottles, shoes)
- **People**: Portrait photos with simple backgrounds
- **Objects**: Clear objects against contrasting backgrounds
- **Complex**: Images with hair, fur, or transparent objects

## Output

Processed images will be saved to your selected output directory with the suffix `_nobg` by default.

Example:
```
Input:  samples/product.jpg
Output: output/product_nobg.png
```

## Tips for Best Results

1. Use high-resolution images (1000px+ on longest side)
2. Ensure good contrast between subject and background
3. Avoid very complex backgrounds
4. Use the "Product Photography" preset for products
5. Enable alpha matting for better edge quality (slower)

---

Happy processing! 🎨
