from dataclasses import dataclass

@dataclass
class Song:
    artist:str = None 
    title:str = None 
    album:str = None 
    seconds:int = None
    length:int = None
    img_url:str = None