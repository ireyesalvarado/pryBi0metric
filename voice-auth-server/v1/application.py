import os
from flask import Flask, request, render_template, jsonify
from VoiceAuthentication import VoiceAuthentication
import app_setup
import speech_recognition as speech_recog
import boto3

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
    #session = boto3.Session(
    # aws_access_key_id='AKIAJQ2P4ECT5NPIE2IA',
    # aws_secret_access_key='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',
    # region_name='us-west-2'
    #)

    s32 = boto3.client('s3',aws_access_key_id='AKIAJQ2P4ECT5NPIE2IA',
     aws_secret_access_key='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')

    #s3 = session.resource('s3')

    data = request.get_json()
    namefileBase = data['namefileBase']
    namefileTemporal = data['namefileTemporal']

    #bucketname = 'bucketassistant' 
    #file_to_read = namefileBase

    #obj = s3.Object(bucketname, file_to_read)
    #body = obj.get()['Body'].read()

    print(app_setup.TEMP_FOLDER,'este es mi filename')
    s32.download_file('bucketassistant',namefileBase,'./temp/'+namefileBase+'.wav')
    s32.download_file('bucketassistant',namefileTemporal,'./temp/'+namefileTemporal+'.wav')


    temp_path_base = os.path.join(app_setup.TEMP_FOLDER, namefileBase+'.wav')
    temp_path_temporal = os.path.join(app_setup.TEMP_FOLDER, namefileTemporal+'.wav')
    #temp_path_temporal = os.path.join('D:\pry0auth\\rec', namefileBase)

    #def get_and_save_temp_file(request_file):
    #    file_storage = request.files[request_file]
    #    temp_path = os.path.join(app_setup.TEMP_FOLDER, file_storage.filename)
    #    file_storage.save(temp_path)
    #    return temp_path

    #f1 = request.files["wav1"]
    #f2 = request.files["wav2"]
    #f1_path = temp_path_base
    #f2_path = temp_path_temporal

    #f1_path = get_and_save_temp_file("wav1")
    #f2_path = get_and_save_temp_file("wav2")

    #result = VOICE_AUTH_MODEL.authenticate(f1_path, f2_path)
    result = VOICE_AUTH_MODEL.authenticate(temp_path_base, temp_path_temporal)
    os.unlink('./temp/'+namefileBase+'.wav') 
    os.unlink('./temp/'+namefileTemporal+'.wav')                                                       
    #result=[2,3,4]
    # return render_template('index.html', display=result[0])
    return jsonify(verification=result[0],
                   percentage="{}%".format(result[2]))

@application.route('/getspeechtext', methods=['POST'])
def getspeechtext():

    s32 = boto3.client('s3',aws_access_key_id='AKIAJQ2P4ECT5NPIE2IA',
    aws_secret_access_key='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')

    data = request.get_json()
    namefile = data['namefile']
    #print(namefile,'este es mi filename')
    #print(app_setup.TEMP_FOLDER)
    s32.download_file('bucketassistant',namefile,'./temp/'+namefile+'.wav')
    
    temp_path = os.path.join(app_setup.TEMP_FOLDER, namefile+'.wav')
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
    
    os.unlink('./temp/'+namefile+'.wav') 
    
    return jsonify(texto=text)



if __name__ == "__main__":
    application.run(debug=True)
    #application.run(host='192.168.1.9', port=5002)
