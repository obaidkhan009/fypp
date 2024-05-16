##this is for the DALL-E image API
# import requests
# import threading
# import os
# import time
# import json

# from openai import OpenAI


# class NextLegAPI:
#     def __init__(self, auth_token):
#         self.imagine_url = "https://api.thenextleg.io/v2/imagine"
#         self.get_message_url = "https://api.thenextleg.io/v2/message/"
#         self.button_press_url = "https://api.thenextleg.io/v2/button/"

#         self.headers = {
#             'Authorization': 'Bearer 47d532f2-5962-4318-bd35-983dcc455e06' ,
#             'Content-Type': 'application/json'
#         }

#     def get_images(self, datas):
#         response_datas = []
#         threads = []

#         for prompt in datas['prompts']:
#             thread = threading.Thread(target=self.request_midjourney, args=(prompt, datas["imageSize"], response_datas))
#             thread.start()
#             threads.append(thread)

#         for thread in threads:
#             thread.join()

#         urls = [image_urls['response']['imageUrls'] for image_urls in response_datas]
#         response_datas = [url for sublist in urls for url in sublist]

#         return response_datas

#     def request_midjourney(self, prompt, image_size, response_datas):
#         payload = json.dumps({
#             "msg": prompt + " --ar " + image_size,
#             "ref": "",
#             "webhookOverride": "",
#             "ignorePrefilter": "false"
#         })

#         response = requests.request("POST", self.imagine_url, headers=self.headers, data=payload)
#         returned_response = self.get_message(response.json()['messageId'])
#         response_datas.append(returned_response)

#     def get_message(self, message_id):
#         message_url = self.get_message_url + message_id + '?expireMins=2'
#         response = requests.request("GET", message_url, headers=self.headers)
#         while int(response.json()['progress']) < 100:
#             time.sleep(10)
#             response = requests.request("GET", message_url, headers=self.headers)
#         return response.json()
    
# class OpenAIapi:
#     def __init__(self):
#         self.client = OpenAI(api_key="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")

#     def get_images(self, input):
#         urls = []
#         threads = []

#         for _ in range(input['num_images']):
#             thread = threading.Thread(target=self.request_dall_e, args=(input['prompt'], urls))
#             thread.start()
#             threads.append(thread)

#         for thread in threads:
#             thread.join()

#         return urls
    
#     def request_dall_e(self, prompt, urls):
#         response = self.client.images.generate(
#         model="dall-e-3",
#         prompt=prompt,
#         n=1,
#         quality="standard"
#         )
#         print(str(response))
#         url = response.data[0].url
#         urls.append(url)
    
import requests
import io
from PIL import Image
import json

class TextToImageAPI:
    def __init__(self, api_tokens):
        """
        Initialize the API with a dictionary of tokens for each model.
        :param api_tokens: Dictionary containing tokens for each model.
        """
        self.api_tokens = api_tokens

    def generate_images(self, model_choice, prompt, num_images=1):
        """
        Generate images based on the selected model.
        :param model_choice: The model to use.
        :param prompt: The text prompt to use for image generation.
        :param num_images: The number of images to generate.
        :return: List of image bytes.
        """
        try:
            # Get the correct API endpoint and token for the chosen model
            api_url, api_token = self.get_api_info(model_choice)
            headers = {
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json",
            }

            images = []
            for _ in range(num_images):
                image_bytes = self.query_image_generation(api_url, headers, prompt)
                images.append(image_bytes)

            return images
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}")

    def get_api_info(self, model_choice):
        """
        Get the API URL and token based on the model choice.
        :param model_choice: The model to use.
        :return: Tuple of (API endpoint, token).
        """
        if model_choice in self.api_tokens:
            api_token = self.api_tokens[model_choice]
            api_url = self.get_model_url(model_choice)
            return api_url, api_token
        else:
            raise ValueError("Invalid model choice")

    def get_model_url(self, model_choice):
        """
        Get the endpoint URL based on the model choice.
        :param model_choice: The model to use.
        :return: URL of the endpoint.
        """
        model_urls = {
            "HuggingFace": "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
            "animagine": "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.1",
            "stableDiffusion": "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
            "AbsoluteReality": "https://api-inference.huggingface.co/models/digiplay/AbsoluteReality_v1.8.1",
            "PlaygroundV2": "https://api-inference.huggingface.co/models/playgroundai/playground-v2.5-1024px-aesthetic",
        }
        return model_urls.get(model_choice, None)

    def query_image_generation(self, api_url, headers, prompt):
        """
        Send a request to the chosen endpoint to generate the image.
        :param api_url: The endpoint URL.
        :param headers: The headers to use for the request.
        :param prompt: The text prompt.
        :return: The generated image as bytes.
        """
        response = requests.post(api_url, headers=headers, json={"inputs": prompt})
        if response.status_code == 200:
            return response.content  # Return the image content
        else:
            raise Exception(f"Failed to generate image: {response.status_code} {response.text}")
