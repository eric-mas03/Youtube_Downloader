import json, urllib, re
from colorama import Fore, init
from pytube import YouTube
init()

# CONFIGURATION
__VIDEO_ROUTE__ = 'yt_downloader/videos'
__IMAGES_ROUTE__ = 'yt_downloader/images/'
__DATA_URL__ = 'yt_downloader/data/videos.json'
__IMAGE_DOWNLOAD__ = True   # Downloads the thumbnail
__VIDEO_DOWNLOAD__ = True   # Downloads the video

# COLORS
CYAN = Fore.LIGHTCYAN_EX
YELLOW = Fore.LIGHTYELLOW_EX
GREEN = Fore.LIGHTGREEN_EX
RED = Fore.LIGHTRED_EX
WHITE = Fore.LIGHTWHITE_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
RESET = Fore.RESET

# Create Class for json data
class Video():
    
    def __init__(self, data_url: str, videos_route: str, images_route: str) -> None:
        self.data_url = data_url
        self.videos_route = videos_route
        self.images_route = images_route
    
    def jsonreader(self, data_url: str) -> None:
        """Reads the json file"""
        with open(data_url, "r", encoding="utf-8") as file:
            data = json.load(file)
            print(f"{CYAN}[{WHITE}-{CYAN}]{YELLOW} Reading json file...{RESET}")
            for x in data:
                print(f"{GREEN}[{WHITE}+{GREEN}]{GREEN} Title -> {x['title']}{RESET}")
                print(f"{GREEN}[{WHITE}+{GREEN}]{GREEN} Description -> {x['description']}{RESET}")
                print(f"{GREEN}[{WHITE}+{GREEN}]{GREEN} Thumbnail -> {x['thumbnail']}{RESET}")

    def getInfo(self, url: str, yt: object | None) -> bool:
        """Gets the information about the video"""
        
        if not yt:
            yt = YouTube(url)

        data = {
            "title": yt.title,
            "description": yt.description,
            "thumbnail": yt.thumbnail_url
        }

        # Opens and saves json file
        with open(self.data_url, "r", encoding="utf-8") as file:
            data_read = json.load(file)
            do = True

            # Check if duplicated    
            for x in data_read:
                if x["thumbnail"] == data["thumbnail"]:
                    do = False
                    break
              
            if do: data_read.append(data)
        
        # Write old and new data on json file
        with open(self.data_url, "w+", encoding="utf-8") as file:
            file.write(json.dumps(data_read, indent= 4, sort_keys=True, ensure_ascii=False))
        
        return do

    
    def imgDownload(self, url: str) -> None:
        """Downloads the thumbnail (miniature)"""
        ytt = YouTube(url)

        try:
            print(f"{CYAN}[{WHITE}-{CYAN}]{YELLOW} Downloading Image...{RESET}")
            name = re.findall(r"https:\/\/i\.ytimg\.com\/vi\/([a-zA-Z0-9-_]+)\/", ytt.thumbnail_url)[0]
            urllib.request.urlretrieve(ytt.thumbnail_url, f"images/{name}.png")
            print(f"{GREEN}[{WHITE}+{GREEN}]{GREEN} Image downloaded! With Name -> {name}{RESET}")
        except: print(f"{RED}[{WHITE}·{RED}] Error, image can not be downloaded{RESET}")
            
    
    def videoDownload(self, url: str, do: bool) -> None:
        """Download the video"""
        yt = YouTube(url)

        if do == True:
            try:
                print(f"{CYAN}[{WHITE}-{CYAN}]{YELLOW} Downloading video...{RESET}")
                yt.streams.get_highest_resolution().download(self.videos_route)
                print(f"{GREEN}[{WHITE}+{GREEN}] Video Downloaded! With Name -> {yt.title}{RESET}")

            except: print(f"{RED}[{WHITE}·{RED}] Error, file could not be downloaded{RESET}")

        else:
            print(f"{RED}[{WHITE}·{RED}] Error, file is duplicated{RESET}")

def main() -> None:
    # Input video url
    url = input(f"{MAGENTA}[{WHITE}·{MAGENTA}] Input video url:{RESET} ")
    yt = YouTube(url)
    video = Video(__DATA_URL__, __VIDEO_ROUTE__, __IMAGES_ROUTE__)
    
    unrepeated = video.getInfo(url, yt)
    
    if __VIDEO_DOWNLOAD__ == True and unrepeated: video.videoDownload(url, unrepeated)
    if __IMAGE_DOWNLOAD__ == True and unrepeated: video.imgDownload(url)
    if not unrepeated: print(f"{RED}[{WHITE}·{RED}] Error, url is listed!{RESET}")
    print(f"{CYAN}[{WHITE}·{CYAN}]{CYAN} Program fished running{RESET}")
