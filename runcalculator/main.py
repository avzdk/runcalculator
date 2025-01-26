from pyscript import document
from typing import Optional, List
from pydantic import BaseModel
import datetime

def minute_txt2flow(minuteTxt: str) -> float:
    # minuteTxt is in the format "mm:ss" 

    minutes=int(minuteTxt.split(":")[0])
    seconds=int(minuteTxt.split(":")[1])
    return minutes + seconds/60

def convert_minutes2time(minutes: float) -> datetime.time:
    hours = int(minutes // 60)
    minutes = int(minutes % 60)
    return datetime.time(hours, minutes)

class RunInterval(BaseModel):
    tempo: Optional[float] = None# in minutes per kilometer
    distance: Optional[float] = None # in kilometers

    def set_duration(self, duration: float):
        if self.tempo is not None:
            self.distance=duration/tempo
        elif self.distance is not None:
            self.tempo=duration/distance
        else:
            raise Exception("Hverken tempo eller distance er givet!")
    
    @property
    def duration(self):
        return self.distance / self.tempo
    
    def parse(self,intervalTxt: str) -> 'RunInterval':
        parts = intervalTxt.split("@")
        if "km" in parts[0]:
            self.distance=float(parts[0].replace("km",""))
            if "min" in parts[1]:
                self.set_duration=minute_txt2flow(parts[1].replace("min",""))
            else:
                self.tempo=minute_txt2flow(parts[1])
        elif "min" in parts[0]:
            self.tempo=minute_txt2flow(parts[1])
            self.set_duration=minute_txt2flow(parts[0].replace("min",""))
        
        return self

    def __str__(self) -> str:
        return f"{self.distance} km @ {self.tempo} min/km"
    
class Run(BaseModel):
    intervals: Optional[List[RunInterval]] = []

def calculate(event): 
    inputtxt = document.querySelector("#inputtxt")
    intervalstxt = inputtxt.value.split('\n')
    run=Run()
    print(intervalstxt)
    for i in intervalstxt:
        interval=RunInterval()
        interval.parse(i)
        run.intervals.append(interval)    
        print(interval)

    output_div = document.querySelector("#output")
    output_div.innerText = "Test"
