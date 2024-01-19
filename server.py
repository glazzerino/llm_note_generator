import logging
from dotenv import load_dotenv
import openai
import os
from flask import Flask, request, jsonify
from processor import PresentationTranscriptProcessor
from multiprocessing import Process
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO)

def save_synthesis_to_md(synthesis):
    with open('output.md', 'w') as file:
        file.write(synthesis + '\n')

def reverse_trancription_list(transcription_list):
    return transcription_list[::-1]

# Define a function to process and save synthesis asynchronously
def process_and_save_synthesis(processor, transcription_list):
    processor.process_transcription(transcription_list)
    synthesis = '\n'.join(processor.synthesis)
    save_synthesis_to_md(synthesis)
    
@app.route('/process', methods=['POST'])
def process_transcription_list():
    transcription_list = request.json.get('transcriptions')
    reverse_trancription_list(transcription_list)
    
    # Save the request to a JSON file
    with open('request.json', 'w') as file:
        json.dump(request.json, file)
    
    # Create an instance of PresentationTranscriptProcessor
    processor = PresentationTranscriptProcessor()
    
    # Start a new process to execute the function asynchronously
    p = Process(target=process_and_save_synthesis, args=(processor, transcription_list))    
    p.start()
    
    # Return a confirmation message to the client
    return jsonify({'message': 'Data received and processing started'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4040)
