from app.webhooks import webhook
from flask import render_template, Flask


@webhook.route('/', methods=['GET'])
def index():
    return render_template("webhooks/home.html")

@webhook.route('/', methods=['POST'])
def post_route():
        try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    #This catches the initial monday code request that is sent from monday.com
    #the first time a request is sent.
    if request.headers['Content-Length'] == '102':
        response = { "challenge" : data['challenge']}
        return response
     
    print("--"*15 + "running Monday microprocess" + "--"*15)
    event = data['event']
    boardId = event['boardId']
    itemId = event['pulseId']
    m = Monday()
    m.setIds(boardId, itemId)
    
    #Send loading status to monday
    m.loadingStatus()
    
    #Retrieve board data from monday
    process= subprocess.run(['python3', 'app/webhooks/microprocess/getBoardData.py', str(boardId), str(itemId)], capture_output=True)
    mondayReturnjson = process.stdout
    data = mondayReturnjson.decode('utf-8')
    print(data)
    m.updatingXytech()
    # mondayMicroProcessEvent(data)
    print("--"*15 + "COMPLETED Monday microprocess" + "--"*15)
    #Update the xytech status for the board
    m.updatingXytech()
    print("--"*15 + "STARTING xytech microprocess" + "--"*15) 
    proc = subprocess.run(['python3', 'app/webhooks/microprocess/pushXytechData.py', data, str(itemId)], capture_output=True)
    print(proc)
    if proc.returncode == 1:
        m.failedStatus()
        return {"Process" :"Failed"}
    m.successStatus()
    print("--"*15 + "running Xytech microprocess" + "--"*15)
    return {"Process": "Complete"}

