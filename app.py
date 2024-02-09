from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Set the maximum content length for file uploads (in bytes)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # 1 GB

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




# Root where the raw data are stored in our case on google colab
root_dir = "/gdrive/MyDrive/FYPD_Dataset/"

# Root where the structured data will be saved - It can be changed and saved in other direction means after cleaning the data
save_dir = root_dir + "derivatives2/"

# Subjects and blacks
N_Subj_arr = [1,2,3,4,5,6,7,8,9,10]  # N_S---> No.of people
N_block_arr = [1,2,3]               # N_B---> No.of blocks/sessions

##################### Filtering
# Cut-off frequencies
Low_cut = 0.5
High_cut = 100

# Apply a notch filter to remove interference at a specific frequency. here we apply a Notch filter in 50Hz

Notch_bool = True

# Downsampling rate
DS_rate = 4

##################### ICA
# If False, ICA is not applyed
ICA_bool = True
ICA_Components = None
ica_random_state = 23
ica_method = 'infomax'
max_pca_components = None
fit_params = dict(extended=True)

##################### EMG Control
low_f = 1
high_f = 20
# Slide window desing
# Window len (time in sec)
window_len = 0.5
# slide window step (time in sec)
window_step = 0.05

# Threshold
std_times = 3

# Baseline
t_min_baseline = 0
t_max_baseline = 15

# Trial time
t_min = 1
t_max = 3.5

# In[]: Fixed Variables
# Events ID
# Trials tag for each class.
# 31 = Arriba / Up
# 32 = Abajo / Down
# 33 = Derecha / Right
# 34 = Izquierda / Left
event_id = dict(Arriba = 31, Abajo = 32, Derecha = 33, Izquierda = 34)

#Baseline id
baseline_id = dict(Baseline = 13)

# Report initialization
report = dict(Age = 0, Gender = 0, Recording_time = 0,  Ans_R = 0, Ans_W = 0)

# Montage
Adquisition_eq = "biosemi128"
# Get montage
montage = mne.channels.make_standard_montage(Adquisition_eq)

# Extern channels
Ref_channels = ['EXG1', 'EXG2']

# Gaze detection
Gaze_channels = ['EXG3','EXG4']

# Blinks detection
Blinks_channels = ['EXG5','EXG6']

# Mouth Moving detection
Mouth_channels = ['EXG7','EXG8']

# Demographic information
Subject_age = [56,50,34,24,31,29,26,28,35,31]

Subject_gender = ['F','M','M','F','F','M','M','F','M','M']
N_S = 2
N_B =1
datatype="eeg"





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
            return 'No selected file'
    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    readBDFfileData(file_path)
    

    return 'File uploaded successfully. File path: {}'.format(file_path)

def readBDFfileData(file_name):
    rawdata = mne.io.read_raw_bdf(input_fname=file_name, preload=True,verbose='WARNING')
    set_reference(rawdata)
    notch_filter(rawdata)

def set_reference(rawdata):
    rawdata.set_eeg_reference(ref_channels=Ref_channels)
  
def notch_filter(rawdata):
    if Notch_bool:
        # Notch filter
        rawdata = mne.io.Raw.notch_filter(rawdata,freqs=50)

def filtering_raw_data:


if __name__ == '__main__':
    app.run(debug=True)
