import os
import boto3
import json
import base64
from io import BytesIO
from random import randint
from PIL import Image


        

# Resize the image to multiples of 64 (one of the dimensions will be 512)
def resize_image(width=512, height=512):
    if width > height :
        x = 512
        ratio = 512/width
        y = int(height * ratio)
        while y%64 != 0:
            y = y + 1
    else :
        y = 512
        ratio = 512/height
        x = int(width * ratio)
        while y%64 != 0:
            y = y + 1     

    return x, y


# get a BytesIO object from file bytes
def get_bytesio_from_bytes(image_bytes):
    image_io = BytesIO(image_bytes)
    image = Image.open(image_io)
    new_width, new_height = resize_image(image.size[0], image.size[1])

    resized_image = image.resize((new_width, new_height))

    output_bytesio = BytesIO()
    resized_image.save(output_bytesio, format='JPEG')  # You can choose the format you need (JPEG, PNG, etc.)


    return output_bytesio


#get a base64-encoded string from file bytes
def get_base64_from_bytes(image_bytes):
    resized_io = get_bytesio_from_bytes(image_bytes)
    img_str = base64.b64encode(resized_io.getvalue()).decode("utf-8")
    return img_str


#load the bytes from a file on disk
def get_bytes_from_file(file_path):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes

#get the stringified request body for the InvokeModel API call
def get_titan_image_background_replacement_request_body(prompt, image_bytes, mask_prompt, negative_prompt=None, outpainting_mode="DEFAULT"):
    
    input_image_base64 = get_base64_from_bytes(image_bytes)

    body = { #create the JSON payload to pass to the InvokeModel API
        "taskType": "OUTPAINTING",
        "outPaintingParams": {
            "image": input_image_base64,
            "text": "Person in a blurry background inside a office which is proper for professional headshot image, 4k, photo realistic",  # Description of the background to generate
            "maskPrompt": "Person",  # The element(s) to keep
            "outPaintingMode": "PRECISE",  # "DEFAULT" softens the mask. "PRECISE" keeps it sharp.
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,  # Number of variations to generate
            "quality": "premium",  # Allowed values are "standard" and "premium"
            "height": 1024,
            "width": 1024,
            "cfgScale": 8.0,
            "seed": randint(0, 100000),  # Use a random seed
        },
    }
    
    if negative_prompt:
        body['outPaintingParams']['negativeText'] = negative_prompt
    
    return json.dumps(body)

#get a BytesIO object from the Titan Image Generator response
def get_titan_response_image(response):

    response = json.loads(response.get('body').read())
    
    images = response.get('images')
    
    image_data = base64.b64decode(images[0])

    return BytesIO(image_data)





def get_titan_image_image_change_request_body(prompt, image_bytes, mask_prompt, negative_prompt=None, outpainting_mode="DEFAULT"):
    image_bytes = image_bytes.getvalue()
    input_image_base64 = get_base64_from_bytes(image_bytes)
    
    
    body = { #create the JSON payload to pass to the InvokeModel API
        "taskType": "IMAGE_VARIATION",
        "imageVariationParams": {
            "images": [
                input_image_base64
            ],  # The image to vary. This array must contain only one element.
            "text": "The same person in professional headshot image.",  # A description of the original image
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,  # Number of variations to generate
            "quality": "premium",  # Allowed values are "standard" and "premium"
            "height": 1024,
            "width": 1024,
            "cfgScale": 9.1,
            "seed": randint(0, 100000),  # Use a random seed
        },
    }
    
    if negative_prompt:
        body['outPaintingParams']['negativeText'] = negative_prompt
    
    return json.dumps(body)





#generate an image using Amazon Titan Image Generator
def get_image_from_model(prompt_content, image_bytes, mask_prompt=None, negative_prompt=None, outpainting_mode="DEFAULT"):
    session = boto3.Session(
        profile_name=os.environ.get("BWB_PROFILE_NAME")
    ) #sets the profile name to use for AWS credentials
    
    bedrock = session.client(
        service_name='bedrock-runtime', #creates a Bedrock client
        region_name=os.environ.get("BWB_REGION_NAME"),
        endpoint_url=os.environ.get("BWB_ENDPOINT_URL")
    ) 
    
    background_body = get_titan_image_background_replacement_request_body(prompt_content, image_bytes, mask_prompt=mask_prompt, negative_prompt=negative_prompt, outpainting_mode=outpainting_mode) #mask prompt "objects to keep" prompt text "description of background to add"
    
    background_response = bedrock.invoke_model(body=background_body, modelId="amazon.titan-image-generator-v1", contentType="application/json", accept="application/json")
    
    background_output = get_titan_response_image(background_response) # BytesIO file
    
    print("############# background modification done!!!!")
    
    body = get_titan_image_image_change_request_body(prompt_content, background_output, mask_prompt=mask_prompt, negative_prompt=negative_prompt, outpainting_mode=outpainting_mode) #mask prompt "objects to keep" prompt text "description of background to add"

    response = bedrock.invoke_model(body=body, modelId="amazon.titan-image-generator-v1", contentType="application/json", accept="application/json")
    
    output = get_titan_response_image(response) # BytesIO file
    
    return output 



