'''
    locust -f ev_load.py EvLocus --host https://stgevspcharger.uplus.co.kr

'''
from locust import HttpUser,TaskSet, SequentialTaskSet,between
import json, random, datetime
from locust.user import task
from settings import get_req_dataset, urls

client_size = 100
client_list = [i for i in range(client_size)]
using_clients = list()

class EvMobileTaskSequence(SequentialTaskSet):

    tid = None
    accessToken = None

    def _init(self):
        self.target = -1

    def get_req_data(self, *args, **kwargs):
        return get_req_dataset(*args, **kwargs, target=self.target)

    def on_start(self):
        while True:
            self.target = random.choice(client_list)
            if self.target not in using_clients:
                using_clients.append(self.target)
                break

        req_name = "login"
        req = self.get_req_data(req_name, init=True)

        response =self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        # accessToken = response.json()['data']['payload']['accessToken']

    def on_stop(self):
        using_clients.remove(self.target)

    @task
    def retrieveChargeStationInfo(self):
        req_name = "retrieveChargeStationInfo"
        req = self.get_req_data(req_name)

        response = self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def retrieveChargerInfo(self):
        req_name = "retrieveChargerInfo"
        req = self.get_req_data(req_name)

        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def insertOrder(self):
        req_name = "insertOrder"
        req = self.get_req_data(req_name)

        response = self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        self.tid = response.json()['ordrNo']

    @task
    def updateOrder(self):
        req_name = "updateOrder"
        req = self.get_req_data(req_name, self.tid)

        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def sendStartChargeStatus(self):
        req_name = "sendStartChargeStatus"
        req = self.get_req_data(req_name, self.tid)

        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def startTransaction(self):
        req_name = "startTransaction"
        req = self.get_req_data(req_name, self.tid)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )


    @task
    def statusNotificationCharging(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, "Charging")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task(36)
    def meterValues(self):
        req_name = "meterValues"
        req = self.get_req_data(req_name, self.tid)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )


    @task
    def stopTransaction(self):
        req_name = "stopTransaction"
        req = self.get_req_data(req_name, self.tid)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def statusNotificationFinishing(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, "Finishing")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
    @task(12)
    def heartbeat(self):
        req_name = "heartbeat"
        req = self.get_req_data(req_name)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

class EvTaskSequential(SequentialTaskSet):

    tid = None
    lid = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}_card"

    def _init(self):
        self.target = -1

    def get_req_data(self, *args, **kwargs):
        return get_req_dataset(*args, **kwargs, target=self.target)

    @task
    def statusNotificationAvailable(self):
        while True:
            self.target = random.choice(client_list)
            if self.target not in using_clients:
                using_clients.append(self.target)
                break
        print(f'실행 Client:{len(using_clients)}개')

        req_name = "statusNotification"
        req = self.get_req_data(req_name, "Available")

        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def authorize(self):
        req_name = "authorize"
        req = self.get_req_data(req_name)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def statusNotificationPreparing(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, "Preparing")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def tariff(self):
        req_name = "tariff"
        req = self.get_req_data(req_name)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def startTransaction(self):
        req_name = "startTransaction"
        req = self.get_req_data(req_name, None)
        response = self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        self.tid = response.json()['transactionId']

    @task
    def statusNotificationCharging(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, "Charging")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task(36)
    def meterValues(self):
        req_name = "meterValues"
        req = self.get_req_data(req_name, self.tid)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def stopTransaction(self):
        req_name = "stopTransaction"
        req = self.get_req_data(req_name, self.tid)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def statusNotificationFinishing(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, "Finishing")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        using_clients.remove(self.target)

    @task(12)
    def heartbeat(self):
        req_name = "heartbeat"
        req = self.get_req_data(req_name)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

class WebUser(HttpUser):
    tasks =[EvMobileTaskSequence]
    wait_time = between(0.3,0.5)

class Charger(HttpUser):
    # tasks ={EvTaskSequential:3, EvMobileTaskSequence:1}
    # tasks =[EvMobileTaskSequence]
    tasks =[EvTaskSequential]
    wait_time = between(0.3,0.5)
