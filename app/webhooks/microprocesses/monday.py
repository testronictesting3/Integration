import requests
import json
import os

class Monday:
    def __init__(self, itemId=None, boardId=None):
        self.itemId = itemId
        self.boardId = boardId
        self.URL = os.environ.get("MONDAY_URL")
        self.KEY = os.environ.get("MONDAY_API_KEY")
        self.HEADERS = {"Authorization": self.KEY,
                        "API-version": "2023-04", "Content-Type": "application/json"}

    ##### UTILITY FUNCTIONS #####
    def setIds(self, itemId, boardId):
        try:
            if itemId.isdigit() == True and boardId.isdigit() == True:
                self.itemId, self.boardId = itemId, boardId
            else:
                return ValueError
        except ValueError as e:
            print(
                "itemId: {} and / or boardId: {} needs to be numerical only".format(itemId, boardId))

    def getUrl(self):
        return self.URL

    def specFilter(self):
        with open('app/webhooks/util/filterMap.json', 'r') as filter:
            data = filter.read()
        data = json.loads(data)

        # returns an array
        return data

    # A function to deliver all requests to monday server and return the json response.
    def deliver(self, payload):
        if payload is None:
            return {"ERROR": "Your attempt to send empty data to query monday has failed. Please try again with a json payload "}

        try:
            response = request.post(url=self.URL, json={
                "query": payload}, headers=self.HEADERS)
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

    def queryWebhookItem(self):
        query = f"""query{{items(ids: {self.itemId}){{id name column_values{{id value }}}}}}"""
        return self.deliver(payload)

    def querySubitemsBoardId(self, boardId):
        query = f"""query{{ boards(ids: {boardId}){{items_page(limit: 1){{ items{{subitems{{board{{ id }}}}}}}}}}}}"""
        return {"query": query}

    #### THE FOLLOWING ARE ONLY TO CREATE BOARD DATA ####
    # 3 create methods are needed: create_group()
    #                              create_item()
    #                              create_subitem()
    def createGroup(self, name):
        payload = f"""mutation{{ create_group(board_id: "5359834992", group_name: "{name}"){{id}}}}"""
        self.deliver(payload)

    def create_item(self, group, episode):
        payload = f"""mutation{{create_item(board_id:5359834992  ,group_id: "{group}",item_name: "{episode}"){{id}}}}"""
        self.deliver(payload)

    def createSubItem(self, item_id, item,  assetId, spec_no, filt, extension):
        query= f"""mutation{{create_subitem(parent_item_id: "{item_id}", item_name: "{item}", column_values:"{{\\\"status\\\": \\\"0\\\", \\\"asset_id\\\": \\\"{assetId}\\\", \\\"service_spec_no6\\\": \\\"{spec_no}\\\", \\\"type_filter\\\": \\\"{filt}\\\", \\\"file_extension\\\": \\\"{extension}\\\"}}"){{id}}}}"""
        self.deliver(query)

    # Need status updates for each possible status : [loading, failed, updating, invalidAsset, servererror? success ]

    def statusUpdate(self, status):
        payload = f"""mutation{{ change_simple_column_value(board_id: {self.boardId}, item_id: {self.itemId}, column_id: "status", "value": "{status}") {{id name}}}}"""
        self.deliver(payload)
