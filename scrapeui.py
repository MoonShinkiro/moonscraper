from tkinter import Tk, simpledialog
from moonscrape import fetch_images

def download_with_tags():
    root = Tk()
    root.withdraw() #Hides main window
    character = simpledialog.askstring("Input", "Enter the Danbooru character tag (Only 1 allowed, or 2 without other tags on free API):", parent=root)

    if character:
        other_tags = simpledialog.askstring("Input", "Enter additional tag (Only 1 allowed on free API):", parent=root)
        tags_list = other_tags.split() if other_tags else []

        print(f"Starting downloads for {character} with tag filters {tags_list}")
        fetch_images("https://danbooru.donmai.us/", character, tags_list)
        print(f"Finished downloads for {character}")

    root.destroy()

    if __name__ == "__main__":
        download_with_tags()
        Tk().mainloop()