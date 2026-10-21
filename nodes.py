import json 
from langchain_core.messages import AIMessage
from agents import extract_repair_tasks,assign_technician_and_urgency
from state import InspectionState

path = "data/inspection_reports.json"

def load_inspection(state:InspectionState):
    inspection_id = input().strip()
    with open(path) as f:
        inspections = json.load(f)['inspections']
    for data in inspections:
        if data['inspection_id'] == inspection_id:
            return {
                "inspection_id" : inspection_id,
                "property" : data["property"],
                "crew" : data["crew"],
                "report" : data["report"],
                "status" : "extracting",
                "messages" : [AIMessage(content="inspection loaded successful")]
            }
    return {
        "inspection_id":inspection_id,
        "property":"",
        "crew":[],
        "report":"",
        "status": "completed",
        "messages" : [AIMessage(content="inspection not loaded successful")]
    }

def extract_repairs(state:InspectionState):
    if not state['report']:
        return {
            "work_orders":[],
            "status":"completed",
            "messages":[AIMessage(content="extracted repairs")]
        }
    tasks  = extract_repair_tasks(state['report'])
    return {
        "work_orders":[{"task":task,"technician":"","urgency":""} for task in tasks],
        "status":"assigning",
        "messages":[AIMessage(content="extracted repairs")]
    }

def assign_technicians(state:InspectionState):
    res = []
    for i in state['work_orders']:
        technician , urgency = assign_technician_and_urgency(i['task'],state['crew'])
        res.append({"task":i['task'],'technician':technician,'urgency':urgency})
    return {
        "work_orders":res,
        "messages":[AIMessage(content="assigned technicians")]
    }

def format_summary(state:InspectionState):
    lines = [
        "PROPERTY REPAIR SUMMARY",
        "",
        f"Inspection ID : {state['inspection_id']}",
        f"Property      : {state['property']}",
        f"Crew          : {", ".join(state['crew'])}",
        "",
        f"Work Orders ({len(state['work_orders'])}):"
    ]
    for i , val in enumerate(state['work_orders'],start=1):
        lines.append(f"   {i}. [{val['urgency']}] {val['task']}")
        lines.append(f"      Technician: {val['technician']}")

    return {
        "summary":"\n".join(lines),
        "status":"completed",
        "messages":[AIMessage(content="summary formatted")]
    }
