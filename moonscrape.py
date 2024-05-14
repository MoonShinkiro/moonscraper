import requests
import os

url = "https://danbooru.donmai.us/"

def fetch_images(base_url, character_tag, other_tags=None):
    if not os.path.exists(character_tag):
        os.makedirs(character_tag)
    #temporary limit of 100 for api reasons
    params = {
        'tags': f'{character_tag} {other_tags}' if other_tags else character_tag,
        'limit': 100,
        'page': 1
    }

    while True:
        response = requests.get(f"{base_url}/posts.json", params=params)
        data = response.json()

        if not data:
            break

        for post in data:
            image_url = post.get('file_url')
            if image_url:
                try:
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                #split paths based on character tag name
                    image_name = image_url.split('/')[-1]
                    with open(os.path.join(character_tag, image_name), 'wb') as f:
                        f.write(image_response.content)
                    print(f"Downloaded {image_name} to {character_tag}/")
                except Exception as e:
                    print(f"Failed to download {image_url}: {e}")

        params['page'] += 1

#insert character tag followed by other tags 
fetch_images(url, "saber", "solo")