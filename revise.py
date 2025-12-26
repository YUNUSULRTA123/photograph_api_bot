import requests
import json
import base64


class ReveAPI:

    def __init__(self, api_key):
        # Base URL and authorization headers required by the Reve API
        self.URL = "https://api.reve.com/v1/"
        self.HEADERS = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def generate_image(
        self,
        prompt,
        aspect_ratio="16:9",
        version="latest",
        save_json="reve_output.json",
        save_image="reve_image.png"
    ):
        # Request body containing generation parameters
        payload = {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "version": version
        }

        # Sending request to Reve API
        response = requests.post(
            self.URL + "image/create",
            headers=self.HEADERS,
            json=payload
        )

        # Trigger an exception if HTTP status is not OK
        response.raise_for_status()

        # Parsed JSON response from the API
        result = response.json()

        # Save JSON response if needed
        if save_json:
            with open(save_json, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"Request ID: {result.get('request_id')}")
        print(f"Credits used: {result.get('credits_used')}")
        print(f"Credits remaining: {result.get('credits_remaining')}")

        # If the API returned an image - decode and save it
        if result.get("image") and save_image:
            self.save_image(result["image"], save_image)

        # Reve warns about content policy violations with this flag
        if result.get("content_violation"):
            print("Warning: content policy violation detected")
        else:
            print("Image generated successfully")

        return result

    def save_image(self, base64_string, file_path):
        # Decode base64 string and save as a file
        decoded_data = base64.b64decode(base64_string)
        with open(file_path, "wb") as img_file:
            img_file.write(decoded_data)
        print(f"Image saved to {file_path}")

REVE_API_KEY = 'papi.1b368fe2-e5d1-49c8-918d-bcda46d418ad.Fm4ByYpwa_CrEd6rSgVLyslo5gfrnXeZ'
# Main API client instance (used by bot later)
reve_api = ReveAPI(REVE_API_KEY)


if __name__ == "__main__":
    # Test example (prompt in English)
    result = reve_api.generate_image(
        "A fluffy cat wearing glasses",
        save_json="reve_output.json",
        save_image="generated_image.png"
    )
    print(result)