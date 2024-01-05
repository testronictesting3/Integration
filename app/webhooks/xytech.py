import os
import requests

class Xytech():

    def __init__(self, assetId=0):
	self.assetId = assetId
	self.serviceSpecNo = 0
	self.serviceRowNo = 0
	self.query = ""

    #Utility Methods
    def __setQuery__(self,query):
	self.query = query

    def __setIds__(self, assetId, serviceSpecId):
	pass

    def patchRequest(self, data):
	pass

    #Live endpoint requests
    def getJob(self, job):
	pass

    def queryForServiceRow(self, work_orders: []) -> str:
	if work_orders == []:
	    return "Empty Work Orders"
	else:
	    url = f""" """"

    #Dev endpoint requests
    #-------possibly change the flask ENV ---------


    def typeFilter(self, type):

	with open("app/webhooks/typesFilter.py", "r") as filter:
	    data = filter.read()

	data = json.loads(data)

	if len(type) == 2:
	    first = type[0]
	    second = int(type[1])
	    t = types.get(a, "type does not exist")
	    return t[second]
	else:
	    return types.get(t, "type does not exist.")
