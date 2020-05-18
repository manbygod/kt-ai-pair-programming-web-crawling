from datetime import datetime

def validate(date_text, format):
    
    try:
        datetime.strptime(date_text, format)
        return date_text
    except:
        print("datetime format error")
        return None
    
def getToday(format):
    return datetime.now().strftime(format)