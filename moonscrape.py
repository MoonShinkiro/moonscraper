import requests
import os
import json

API_KEY = os.getenv('DANBOORU_API_KEY')
USERNAME = os.getenv('DANBOORU_USERNAME')
url = "https://danbooru.donmai.us/"

def fetch_images(base_url, character_tag, other_tags=[]):
    tags = ' '.join([character_tag] + other_tags).strip()
    character_directory = os.path.join('images', character_tag.replace(' ', '_'))
    os.makedirs(character_directory, exist_ok=True)
    
    params = {
        'login': USERNAME,
        'api_key': API_KEY,
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
        
        if not data:
            print("No more images available.")
            break
        
        for post in data:
            image_url = post.get('file_url')
            if image_url:
                try:
                    image_response = requests.get(image_url)
                    image_response.raise_for_status()
                    
                    image_name = image_url.split('/')[-1]
                    image_path = os.path.join(character_directory, image_name)
                    with open(image_path, 'wb') as f:
                        f.write(image_response.content)
                    print(f"Downloaded {image_name} to {character_directory}/")
                    
                    tag_string = post.get('tag_string', '')
                    tags = [tag.replace('_', ' ') for tag in tag_string.split()]
                    tag_string = ', '.join(tags)
                    
                    txt_filename = os.path.splitext(image_name)[0] + '.txt'
                    txt_path = os.path.join(character_directory, txt_filename)
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write(tag_string)
                    print(f"Saved tags for {image_name} to {txt_filename}")
                    
                except Exception as e:
                    print(f"Failed to download {image_url} or save tags: {e}")
        
        params['page'] += 1