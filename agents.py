import os 
from google import genai 
from dotenv import load_dotenv 

load_dotenv(override=True)

model = os.getenv("GEMINI_MODEL")

def extract_repair_tasks(report:str):
    prompt = (
        "Give every pair or follow up job arising from the inspection"
        "reply with one job per line , each opening with marker REPAIR: followed by job"
        f"Inspection report:{report}"

    )
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(model=model,contents=prompt)
    return [
        line.strip().removeprefix("REPAIR:").strip()
        for line in response.text.splitlines()
        if line.strip().startswith("REPAIR:")
    ]

def assign_technician_and_urgency(task:str,crew:list[str]):
    prompt = (
        "select exactly one technician from crew list supplied"
        "require urgency to be one of High , Medium, or Low"
        "reply exactly with two lines,the first opening with TECHNICIAN: and second with URGENCY:"
        "TECHNICIAN:<name>\n"
        "URGENCY:<High,Medium,orLow>\n"
        f"task:{task}\n"
        f"crew:{', '.join(crew)}"
    )

    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(model=model,contents=prompt)

    fields = {}
    for line in response.text.splitlines():
        label , sep , val = line.strip().partition(":")
        if sep and label in {'TECHNICIAN','URGENCY'}:
            fields[label] = val.strip()
    technician , urgency = fields["TECHNICIAN"] , fields["URGENCY"]
    return technician , urgency 






