### clone
git clone --branch dev https://github.com/linhthi/hannom_anntotation_tool.git

### Data
https://drive.google.com/drive/folders/1bWIKV3CYlKuaOIfxXTlWXMMuTGDh8zMW?usp=sharing

### Backend
Config at: config.py

Install packages:
```
pip3 install -r requirements.txt
```
```bat
yum update -y && yum install -y libXext libSM libXrender
sudo apt-get install -y libsm6 libxext6 libxrender-dev
```
Run backend:
```
python3 app.py
```

### Frontend
Config at: front_end/tool_annotator/.env

Move to frontend directory:
```
cd front_end/tool_annotator
```
Install all dependency:
```
npm install
```
Start front_end:
```
npm start
```

### Access
http://localhost:3003/images
