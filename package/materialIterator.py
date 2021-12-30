import math
from typing import Iterator

MIN_SCALE = 0.1
MAX_SCALE = 360

MIN_SPEED = 0.05
MAX_SPEED = 20

DEFAULT_INTERVALs = 100

class MaterialIterator:
  def __init__(self, speed = 1, lower = 0, upper = 360):
    self.speed = self.sanitiseSpeed(speed)
    range = self.sanitiseRange(lower, upper)
    self.lower = range[0]
    self.upper = range[1]
    self.reset()

  def sanitiseSpeed(self, speed):
    if (speed <= MIN_SPEED):
      print("Minimum speed reached: %d is smaller than %d", speed, MIN_SPEED)
      return MIN_SPEED
    elif (speed > MAX_SPEED):
      print("Maximum speed exceeded: %d is greater than %d", speed, MAX_SPEED)
      return MAX_SPEED
    else:
      return speed

  def sanitiseRange(self, lower, upper):
    if (lower < 0 or upper < 1):
      print("Minimum range reached: %d must be greater than 0 and %d must be greater than 1")
      return (0, 360)
    elif (lower > 359 or upper > 360):
      print("Maximum range exceeded: %d must be smaller than 359 and %d must be smaller than 360 degrees", lower, upper)
      return (0, 360)
    else:
      return (lower, upper)

  def reset(self):
    self.offset = 0
  
  def __iter__(self):
    self.reset()
    return self

  def __next__(self):
    if (self.offset > float(DEFAULT_INTERVALs / float(self.speed))):
      raise StopIteration
    theta = self.lower * math.pi / 360 + (self.offset * math.pi * self.speed * (self.upper - self.lower) / 360) / DEFAULT_INTERVALs
    next = 1 - math.cos(theta)
    self.offset += 1
    return next