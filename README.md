# Automated Medical Consulting
## Installation

1. Git Clone this repository - git clone https://github.com/mhosankalp/automc
2. Download the biobert weights and checkpoints from https://github.com/naver/biobert-pretrained and place it into directory 
BIOBERT_DIR. Make sure to name it as biobert_model.ckpt for all three files. You can also fine tune your model by gathering more QA data and place it into directory BIOASQ_DIR. Modify the flag.py to update the parameters as needed if your training. If you are just running the model you need not make any changes to flag.py
3. cd automc 
4. Create a virual enviornment
5. source activate virtual enviornment
6. pip install -r requirements.txt
7. python app.py
8. Navigate to 127.0.0.1:5000 in your browser (safari/chrome)

## Screenshots for the webapp

1. Login screen:

![GitHub Logo](/media/Image1.png)

2. Payment Screen:

![GitHub Logo](/media/Image2.png)

3. Home Page:

![GitHub Logo](/media/Image3.png)

4. First application of answering questions using biobert. Rest of the application are under development. 

![GitHub Logo](/media/Image4.png)

5. Current answer as recieved now

![GitHub Logo](/media/Image5.png)
