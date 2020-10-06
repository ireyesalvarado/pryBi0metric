import os
from flask import Flask, request, render_template, jsonify
from VoiceAuthentication import VoiceAuthentication
import app_setup
import speech_recognition as speech_recog


application = Flask(__name__)

VOICE_AUTH_MODEL = VoiceAuthentication('mobile_model.pt')


@application.route('/')
def home():
    return render_template('index.html')

@application.route('/speech')
def speech():
    return render_template('speech.html')

@application.route('/verify', methods=['POST'])
def verify():
    '''
    verify from wav files
    '''
    def get_and_save_temp_file(request_file):
        file_storage = request.files[request_file]
        temp_path = os.path.join(app_setup.TEMP_FOLDER, file_storage.filename)
        file_storage.save(temp_path)
        return temp_path

    # f1 = request.files["wav1"]
    # f2 = request.files["wav2"]
    f1_path = get_and_save_temp_file("wav1")
    f2_path = get_and_save_temp_file("wav2")

    result = VOICE_AUTH_MODEL.authenticate(f1_path, f2_path)

    # return render_template('index.html', display=result[0])
    return jsonify(verification=result[0],
                   percentage="{}%".format(result[2]))

@application.route('/getspeechtext', methods=['POST'])
def getspeechtext():

    data = request.get_json()
    namefile = data['namefile']
    #print(namefile,'este es mi filename')
    #print(app_setup.TEMP_FOLDER)
    
    temp_path = os.path.join('D:\-sist-nt-o-uth-400\wav', namefile)
    f1_path = temp_path
    #def get_and_save_temp_file(request_file):
    #    file_storage = request.files[request_file]
    #    temp_path = os.path.join(app_setup.TEMP_FOLDER, file_storage.filename)
    #    file_storage.save(temp_path)
    #    return temp_path

    #f1_path = get_and_save_temp_file("wav1")
    r = speech_recog.Recognizer()
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False
    with speech_recog.WavFile(f1_path) as source:
         audio_data = r.record(source)
         text = r.recognize_google(audio_data, language='es-ES')
    
    
    return jsonify(texto=text)



if __name__ == "__main__":
    #application.run(debug=True)
    application.run(host='192.168.1.4', port=5002)
