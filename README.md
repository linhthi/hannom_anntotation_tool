### clone
git clone --branch dev https://github.com/linhthi/hannom_anntotation_tool.git

### Data
https://drive.google.com/drive/folders/1bWIKV3CYlKuaOIfxXTlWXMMuTGDh8zMW?usp=sharing

### Backend
Install packages:
```
pip install -r requirements.txt
```
```bat
yum update -y && yum install -y libXext libSM libXrender
sudo apt-get install -y libsm6 libxext6 libxrender-dev
```
Run backend:
```
python app.py
```

### Frontend
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
http://localhost:3000/images
