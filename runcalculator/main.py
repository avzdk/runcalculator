from pyscript import document
from typing import Optional, List
from pydantic import BaseModel
from datetime import timedelta

def txt2time(timeTxt: str) -> timedelta:
    # minuteTxt is in the format "mm:ss" 
    splittxt=timeTxt.split(":")
    if len(splittxt)==2:
        minutes=int(splittxt[0])
        seconds=int(splittxt[1])
        return timedelta(minutes=minutes,seconds=seconds)
    else:
        hours=int(splittxt[0])
        minutes=int(splittxt[1])
        seconds=int(splittxt[2])
        return timedelta(hours=hours,minutes=minutes,seconds=seconds)

def timedelta2txt(duration: timedelta) -> str:
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

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
        txt=f"{self.distance:.1f} @ {timedelta2txt(self.tempo)} = {timedelta2txt(self.duration)}"


        return txt
    
class Run(BaseModel):
    intervals: Optional[List[RunInterval]] = []

    @property
    def duration(self) -> timedelta:
        return sum([i.duration for i in self.intervals],timedelta())
    
    @property
    def distance(self) -> float:
        return sum([i.distance for i in self.intervals])

    @property
    def tempo(self) -> timedelta:
        return self.duration/self.distance
    
    @property
    def intervalsTxt(self) -> str:
        return "\n".join([str(i) for i in self.intervals])
    
    def __str__(self) -> str:
        return f"Distance: {self.distance:.1f} km\nVarighed: {self.duration}\nTempo: {str(self.tempo)}\n\n{self.intervalsTxt}"

def calculate(event): 
    inputtxt = document.querySelector("#inputtxt")
    intervalstxt = inputtxt.value.split('\n')
    run=Run()
    for i in intervalstxt:
        if "@" in i:    
            interval=RunInterval()
            interval.parse(i)
            run.intervals.append(interval)    
        
    output_div = document.querySelector("#output")
    text=str(run)
    output_div.innerText = text
