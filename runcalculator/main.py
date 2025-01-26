from pyscript import document
from typing import Optional, List
from pydantic import BaseModel
from datetime import timedelta

def txt2time(minuteTxt: str) -> timedelta:
    # minuteTxt is in the format "mm:ss" 

    minutes=int(minuteTxt.split(":")[0])
    seconds=int(minuteTxt.split(":")[1])
    return timedelta(minutes=minutes,seconds=seconds)

class RunInterval(BaseModel):
    tempo: Optional[timedelta] = None# in minutes per kilometer
    distance: Optional[float] = None # in kilometers

    def set_duration(self, duration: timedelta):
        if self.tempo is not None:
            self.distance=duration/self.tempo
        elif self.distance is not None:
            self.tempo=duration/self.distance
        else:
            raise Exception("Hverken tempo eller distance er givet!")
    
    @property
    def duration(self) -> timedelta:
        tempo_minutes=self.tempo.total_seconds()/60
        return timedelta(minutes=tempo_minutes*self.distance)
        
    
    def parse(self,intervalTxt: str) -> 'RunInterval':
        parts = intervalTxt.split("@")
        if "km" in parts[0]:
            self.distance=float(parts[0].replace("km",""))
            if "min" in parts[1]:
                self.set_duration(txt2time(parts[1].replace("min","")))
            else:
                self.tempo=txt2time(parts[1])
        elif "min" in parts[0]:
            self.tempo=txt2time(parts[1])
            self.set_duration(txt2time(parts[0].replace("min","")))
        
        return self

    def __str__(self) -> str:
        return f"{self.distance} km @ {self.tempo} min/km = {self.duration} min"
    
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
