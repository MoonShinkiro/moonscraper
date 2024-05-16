import requests
import os
import json

url = "https://danbooru.donmai.us/"

def fetch_images(base_url, character_tag, other_tags=[]):
    tags = ' '.join([character_tag] + other_tags).strip()
    character_directory = os.path.join('images', character_tag.replace(' ', '_'))
    os.makedirs(character_directory, exist_ok=True)

    #temporary limit of 100 for api reasons
    params = {
        'tags': tags,
        'limit': 100,
        'page': 1
    }

    while True:
        full_url = f"{base_url}posts.json"
        response = requests.get(full_url, params=params)
        try: 
            data = response.json()
            if isinstance(data, dict) and 'success' in data and not data['success']:
                print("Error from API:", data.get('message', 'No error message available.'))
                break
        except json.JSONDecodeError:
            print("Failed to decode JSON from response:", response.text)
            break
        #return when images and break
        if not data:
            print("No more images available.")
            break

        for post in data:
            image_url = post.get('file_url')
            if image_url:
                try:
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                #split paths based on character tag name
                    image_name = image_url.split('/')[-1]
                    with open(os.path.join(character_directory, image_name), 'wb') as f:
                        f.write(image_response.content)
                    print(f"Downloaded {image_name} to {character_directory}/")
                except Exception as e:
                    print(f"Failed to download {image_url}: {e}")

        params['page'] += 1