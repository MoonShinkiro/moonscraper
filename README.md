# moonscraper
Character-based Danbooru image scraper for organizing datasets based on given character and other tags.
Mainly focused on gathering character data for image-based Machine Learning training.

# Requirements:
Run in terminal: ```pip install -r requirements.txt```

# Usage:
1. Write your API Key and username into the `.env` file if available in order to user more than 2 tags. (This script is designed for running character tags so without API key access you will only be able to scrape using 1 character tag and 1 additional tag.)
2. Run in terminal: ```python run_scraper.py``` in the folder location.
3. Use CTRL + C or any function to cancel terminal if you wish to stop the scrape early.
4. Find your images in the /images folder.

# TODO:
- Create running in .bat
- Cancel scrape more safely
