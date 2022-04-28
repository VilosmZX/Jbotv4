from datetime import datetime

def generate_time():
  return datetime.now().strftime("%H:%M")