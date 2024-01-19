import json
import requests

def test_process_transcription_list():
    # Load the saved request.json
    with open('request.json', 'r') as file:
        request_data = json.load(file)
    
    # Send the request to the /process endpoint
    response = requests.post('http://localhost:4040/process', json=request_data)
    
    # Assert that the response status code is 200
    assert response.status_code == 200
    
    # Assert that the response message is as expected
    expected_message = {'message': 'Data received and processing started'}
    assert response.json() == expected_message

# Run the test
test_process_transcription_list()