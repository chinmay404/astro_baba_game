import requests

url = "https://api.limewire.com/api/image/generation"

payload = {
  "prompt": "A cute baby sea otter",
  "aspect_ratio": "1:1"
}

headers = {
  "Content-Type": "application/json",
  "X-Api-Version": "v1",
  "Accept": "application/json",
  "Authorization": "Bearer lmwr_sk_z4Z1jKjdBs_T3gh8xpbafQLzUkHD4S90Otleur4p9evQgZEu"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()
print(data)



self.full_prediction.append(ai_response.get('predictions', {}))
                print(ai_response.get('predictions', {}))
                print(ai_response.get('pictureDescription'))
                try:
                    response_json = json.loads(ai_response.content)
                    self.predictions = response_json.get(
                        "PREDICTIONS", "No predictions provided")
                    self.image_description = response_json.get(
                        "IMAGE_DESCRIPTION", "No image description provided")
                    
                    print(self.predictions)
                    print(self.image_description)
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    return f"Error parsing response: {e}"
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    return f"An unexpected error occurred: {e}"

