# image-steganography-GUI

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Stepy by step working logic](#steps)

![first_screen](https://user-images.githubusercontent.com/101993364/200196667-0f6a0777-24a7-4831-a6ab-bb59abff38a6.png)

  
Hide data by embedding in the text file into a image with a modern and simple tkinter GUI
(Or extract data from a data-embedded image)
# Note:
=> This GUI-application uses the Least Significant Bit (LSB) steganography method without encryption <=
The GUI does not encrypt the text file provided as input. I haven't included this functionality in the code yet.(it directly embeds the data from the text file into the image without any encryption) Therefore, if you're going to hide very important data, encrypt the data within the text file first and then provide it to the GUI.


# Installation

To use this project, follow these steps:

1. Install the required libraries. Use the following commands to install the PIL (Python Imaging Library) and tkinter libraries using pip:

   ```bash
   # - WINDOWS Installation -
   pip install pillow
   pip install tk

   # - LINUX Installation -
   sudo apt-get install python3-pil python3-pil.imagetk
   sudo apt-get install python3-tk

# Usage
1. Run the main.py file located in the project's root directory. You can do this with the following command:
   ```bash
   python main.py

# Steps
->[Stepy by step working logic]:
1. Select an Image File
2. Select a text file
3. Select a Destination Folder
4. Click the "Embed Data" Button
5. ^_^ After clicking the "Embed Data" button, your newly embedded image will be saved in the chosen destination folder. If you want to extract the data later, you can select the embedded image and use a simple extraction process.

![second_screen](https://user-images.githubusercontent.com/101993364/200196811-3280b863-334e-4e96-a883-5eed2f9cf463.png)

![img](https://user-images.githubusercontent.com/101993364/200428001-8cb82509-6221-427d-9537-615accbef44f.jpeg)
