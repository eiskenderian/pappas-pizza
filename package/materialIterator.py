import math
from typing import Iterator

MIN_SCALE = 0.1
MAX_SCALE = 360

MIN_SPEED = 0.05
MAX_SPEED = 20

DEFAULT_INTERVALs = 100

class MaterialIterator:
  def __init__(self, speed = 1, scale = 1):
    self.speed = self.sanitiseSpeed(speed)
    self.scale = self.sanitiseScale(scale)
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

  def sanitiseScale(self, scale):
    if (scale < 1):
      print("Minimum scale reached: %d is smaller than %d", scale, MIN_SCALE)
      return 1
    elif (scale > MAX_SCALE):
      print("Maximum scale exceeded: %d is greater than %d", scale, MIN_SCALE)
      return MAX_SCALE
    else:
      return scale

  def reset(self):
    self.offset = 0
  
  def __iter__(self):
    self.reset()
    return self

  def __next__(self):
    if (self.offset > float(DEFAULT_INTERVALs / float(self.speed))):
      raise StopIteration
    theta = (self.offset * math.pi * self.speed) / DEFAULT_INTERVALs
    next = 1 - math.cos(theta)
    self.offset += 1
    return next