from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time
import constants

'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
def getOCR_output(filepath):
    subscription_key=constants.VISION_KEY
    endpoint = constants.VISION_ENDPOINT

    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    result=''

    with open(filepath, "rb") as image_stream:
        result = computervision_client.read_in_stream(image_stream, language="en", raw=True)

    # Call API with URL and raw response (allows you to get the operation location)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = result.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        return read_result