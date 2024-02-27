import sys
import json
import requests
from monday import Monday

jsonVals = {
    "status":"test",
     "status_1":"test",
     "asset_id":"test",
     "delivery_eta":"test",
     "qc_pass_date":"test" ,
     "revision_number":"test",
     "revision_date":"test",
     "final_delivery":"test",
     "service_spec_no6":"test",
     "type_filter":"test"}

if __name__=="__main__":
    s = sys.argv[1:]
    board = Monday()
    boardId, itemId = s[0], s[1]
    # set the board and item id and query webhook item
    board.setIds(boardId, itemId)
    response = board.queryWebHookItem()
    data = response['data']
    if data == None:
        board.invalidAssetStatus()
        
    column_values = data['items'][0]['column_values']
    for i in range(0, len(column_values)):
        id = column_values[i]['id']
        val = column_values[i]['value']
        jsonVals[id] = val
    print(json.dumps(jsonVals))
    