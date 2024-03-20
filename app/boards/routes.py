import json
import subprocess
from app.boards import bp
from flask import Flask, render_template, request, redirect, url_for, jsonify

#Board Route has many different responsibilities: 
# _1 Process job numbers 
# ---- The custom route should receive the job number and process that job number into a request for work orders (wo_no_seq)
# _2 Process work order numbers
#----- The work order should let you know what episode we are working on.
# _3 Process service rows 
# ----Service rows are the deliverables for each episode 
# ---- 
# _4 pushing service rows onto the monday board.
# have a microservice for each part of the board interaction
### a - Service for Creating a groupo on the board
### b - a Service for creating an item on the board the item will be the episodes on the board.
### c - a service for creating the subitems on the items on the board.

#Main endpoint 
@bp.route("/" , methods=["GET"])
def main():
    return render_template("board_home/board.html")


#Endpoint to enter the job data to push to the board
@bp.route("/requestJob", methods=["GET"])
def devGetJobs():
    return render_template("/board_home/jobData.html")

# ## DEV ROUTES
# #DEV Endpoint to enter the job data to push to the board
# @bp.route("/DEV1", methods=["GET"])
# def devGetJobs():
#     return render_template("/board_home/jobData.html")

# DEV endpoint for retrieving job data
@bp.route("/DEV2", methods=["GET", "POST"])
def devTestBoard():
    data = {}
    data["wo_nos"] = []
    episodesData = {}
    
    numbers = []
    count = 0
    
    job_no = request.form.get("job_no")
    proc = subprocess.run(["python3", "app/webhooks/getJobData.py", str(job_no)], capture_output=True) 
    retData = proc.stdout
    output = retData.decode("utf-8")
    out = json.loads(output)

    #save the description data and the work order number for each episode and pass it to the next endpoint 

    for x in out:
       wo_no = x["wo_no_seq"]["wo_no_seq"]
       wo_desc = x["wo_desc"]
       episode = x["lib_title_APPLE_TITLE_field_55"]
       if episode == None:
        episode = count
        count += 1
       title = x["lib_title_security_title"]

       numbers.append(wo_no)
       #episodesData["wo_no"] = wo_no
       episodesData["wo_desc"] = wo_desc
       episodesData["episode"] = episode
       data[wo_no] = episodesData.copy()
       episodesData.clear()
    data["wo_nos"] = numbers
    data['title'] = title
    data = json.dumps(data)
    return render_template("board_home/jobInfo.html", data=data)

@bp.route("/DEV3", methods=["GET", "POST"])
def devServiceRowTest():
   # objectBuilder = {}
    returnData = {}
    serviceData= request.form.get("info")
    serviceData = json.loads(serviceData)
    array = serviceData["wo_nos"]
    count = 0

    for x in array:
        count += 1
        proc = subprocess.run(["python3", "app/webhooks/getServiceRows.py", x], capture_output=True)
        outData = proc.stdout
        out = outData.decode("utf-8")
        output = json.loads(out)
        #returnData.append({output["work_order_number"], output["deliverables"]})
        desc = serviceData[x]["wo_desc"]
        #objectBuilder[desc] = output

        #Temporary Code to replace the key  with episode number instead of count 
        #This should be deleted once the episode value is properly in place 
        ke =  "episode" + str(serviceData[x]["episode"])
        returnData[ke] = output.copy()
    
    # #Live ENDPOINTs
    # #return render_template("board_home/serviceRows.html", data=returnData)
    boardData = json.dumps(returnData)
    return render_template("board_home/serviceRows.html", data=boardData, showData=returnData )

@bp.route("/pushMonday", methods=["GET", "POST"])
def pushToMondayTest():
    print("Monday Process")
    data = request.form.get("board_data")
    #data = json.loads(data)
    proc = subprocess.run(['python3', 'app/webhooks/pushToMonday.py', data], capture_output=True)
    return render_template("board_home/test.html", data=data)

#Testing endpoint for using the custom tables
@bp.route("/custom", methods=["GET", "POST"])
def testBoard():
    job_no = request.form.get("job_no")
    #Run a subprocess to retrieve the job information data from the xytech endpoint ( database)
    proc = subprocess.run(["python3", "app/webhooks/getJobData.py", str(job_no)], capture_output=True)
    #Should return a list of work order numbers wo_no_seq
    retData = proc.stdout
    output = retData.decode("utf-8")
    out = json.loads(output)
    
    data = {}
    data["out"] = out
    data["tmp"]= [x["wo_no_seq"]["wo_no_seq"] for x in out]
    jsonData = jsonify(data).get_data(as_text=True)                                                                
    return render_template("board_home/jobInfo.html", data=jsonData)

# @bp.route("/serviceRow", methods=["GET", "POST"])
# def serviceRowTest():
#     data = {}
#     data["tmp"] = request.form.get("work_order_data")
#     num = data["tmp"][0]
    
#     #######
#     #The code below is properly working, so make sure the num from above thats being passed into the subprocess is valid first. 
#     #######
    
#     proc = subprocess.run(["python3", "app/webhooks/getServiceRows.py", "17352-1"], capture_output=True)
#     outData = proc.stdout
#     out = outData.decode("utf-8")
#     output = json.loads(out)
#     data=output

#     #some sort of pagination needs to be here for the case where many are returned. 
#     #Take the work order numbers and query for the service row numbers here 
#     # 
#     return render_template("board_home/serviceRows.html", data=data)


@bp.route("/process_data", methods=["GET","POST"])
def processData():
    #Retrieve the job number from t request
    job_no = request.form.get("job_no")
    #Run a subprocess to retrieve the job information data from the xytech endpoint ( database)
    proc = subprocess.run(["python3", "app/webhooks/getJobData.py", str(job_no)], capture_output=True)
    #Should return a list of work order numbers wo_no_seq
    retData = proc.stdout
    data = retData.decode("utf-8")
    print(data)
    return f"data: {data}"

@bp.route("/getJobData", methods=["POST"])
def boardData():

    #Form should be tested for data, should receive data for job number
    jobNo = request.form
    jobProcess = subprocess.run(["python3", "app/webhooks/getJobData.py", str(jobNo)],capture_output=True)
    #retrieve the process output and convert from bytecode
    j = jobProcess.stdout
    jj = j.decode("utf-8")
    #format: data should come back as a string of objects
    data = json.loads(jj)
    info = data[0]["wo_no_seq"]["wo_no_seq"]
    
    return render_template("board_home/jobData.html", data=info)
