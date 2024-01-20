import os
import requests

class Xytech():

    def __init__(self, assetId=0):
	#LIVE
	self.URL = os.environ.get("XYTECH_LIVE_URL")
	self.UN = os.environ.get("XYTECH_LIVE_USER")
    self.PW = os.environ.get("XYTECH_LIVE_SECRET")
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

	def deliver(self, payload):
        if payload is None:
            return {"ERROR": "No Data was received "}

        try:
		    payload = self.URL + data
            response = request.get(url=payload, auth=(self.UN, self.PW))
            response.raise_for_status()
            json_response_data = response.json()

        # handle the possible exceptions here for network or request failures
        except request.exceptions.HTTPError as e:
            print(f" Http error was thrown : {e}")
        except request.exceptions.RequestExceptions as e:
            print(f"Request exception: {e}")
        except Exception as e:
            print(f"Unknown exceptions occured. details: {e}")

        return json_response_data

    #Live endpoint requests
    def getJob(self,job):
        url = f"""MoMediaOrderList?query={{"job_no":{job}, "wo_type_no": 3, "phase_code":"Conf"}}&resultcolumns={{"L":["wo_desc", "wo_no_seq", "job_desc",  "lib_title_episode", "lib_title_security_title", "lib_title_APPLE_TITLE_field_55"]}}"""
        self.deliver(url)

    def queryForServiceRow(self, w_order_num) -> str:
	if work_orders == []:
	    return "Empty Work Orders"
	else:
	    url = f"""MoMediaOrderList?query={{"wo_no_seq": "{w_order_num}"}}&resultcolumns={{"L":["service_row_no", "service_spec_desc","service_profile_desc","APPLE_SRV_field_1", "APPLE_SRV_field_27"]}}""""

	def serviceRowPatch(self,num):
    	query = f"""MoServiceRowList?query={{'service_row_no':{{'$in':[{num}]}}}}"""
	    return self.DEVURL + query 

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

	def typeConversion(self,type):
        conversions = {
            "delivery_eta": "APPLE_SRV_field_108",
            "qc_pass_date": "APPLE_SRV_field_111",
            "revision_number":"APPLE_SRV_field_29",
            "date_revised": "APPLE_SRV_field_102",
            "final_delivery": "APPLE_SRV_field_104"
        }
        return conversions.get(type, "Type doesnt exist here")
