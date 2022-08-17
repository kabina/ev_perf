'''
    locust -f ev_load.py Charger --host https://stgevspcharger.uplus.co.kr

'''
from locust import HttpUser, SequentialTaskSet,between
import json, random, datetime
from locust.user import task
from settings import get_req_dataset, urls

client_size = 300
client_list = [i for i in range(client_size)]
using_clients = list()

def get_target():
    while True:
        target = random.choice(client_list)
        if target not in using_clients:
            using_clients.append(target)
            return target

def remove_target(target):
    using_clients.remove(target)

class OneServer(SequentialTaskSet):

    tid = None
    accessToken = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = -1
        self.accessToken = None
        self.ri = None
        self.tid = None

    def get_req_data(self, *args, **kwargs):
        return get_req_dataset(*args, **kwargs, target=self.target, accessToken=self.accessToken, ri=self.ri)

    @task
    def login(self):

        self.meter = 0
        self.accessToken

        req_name = "login"
        self.target = get_target()

        req = self.get_req_data(req_name, init=True)

        response =self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        self.accessToken = response.json()['data']['payload']['accessToken']

    @task
    def retrieveChargeStationInfo(self):
        req_name = "retrieveChargeStationInfo"
        req = self.get_req_data(req_name)

        self.ri = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}_card"

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
        remove_target(self.target)

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
        # print(self.tid)

    @task
    def updateOrder(self):
        req_name = "updateOrder"
        req = self.get_req_data(req_name, self.tid, self.accessToken)

        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )


class EvMobileTaskSequence(SequentialTaskSet):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = -1
        self.accessToken = None
        self.tid = None
        self.ri = None

    def get_req_data(self, *args, **kwargs):
        return get_req_dataset(*args, **kwargs, target=self.target, accessToken=self.accessToken, tid=self.tid,
                               ri = self.ri)
    @task
    def login(self):


        # while True:
        #     self.target = random.choice(client_list)
        #     if self.target not in using_clients:
        #         using_clients.append(self.target)
        #         break
        # print(f'App Client:{len(using_clients)}개')
        # print(f'App {using_clients}')

        req_name = "login"
        self.target = get_target()
        print(f"Running Client Size:{len(using_clients)}")
        self.meter = 0
        req = self.get_req_data(req_name, init=True)
        self.meter = 0

        response =self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        self.accessToken = response.json()['data']['payload']['accessToken']

    @task
    def retrieveChargeStationInfo(self):
        req_name = "retrieveChargeStationInfo"
        self.ri = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}_app"
        req = self.get_req_data(req_name)
        # self.target = get_target()


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
        # print(self.tid)

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
        req = self.get_req_data(req_name)

        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
    #
    # @task
    # def startTransactionRemote(self):
    #     req_name = "startTransactionRemote"
    #     req = self.get_req_data(req_name)
    #     self.client.post(
    #         url=urls[req_name],
    #         data=json.dumps(req["body"]),
    #         auth=None,
    #         headers=req["header"],
    #         name=req_name,
    #     )


    @task
    def statusNotificationCharging(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, status="Charging")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task(10)
    def meterValues(self):
        req_name = "meterValues"
        self.meter += 10
        req = self.get_req_data(req_name, meter=self.meter)
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    # @task
    # def retrieveChargingValues(self):
    #     req_name = "retrieveChargingValues"
    #     req = self.get_req_data(req_name)
    #     response = self.client.post(
    #         url=urls[req_name],
    #         data=json.dumps(req["body"]),
    #         auth=None,
    #         headers=req["header"],
    #         name=req_name,
    #     )
    #     print(response)

    @task
    def remoteStopTransaction(self):
        req_name = "remoteStopTransaction"
        req = self.get_req_data(req_name)
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
        req = self.get_req_data(req_name)
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
        req = self.get_req_data(req_name, status="Finishing")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        remove_target(self.target)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = -1
        self.ri = None
        self.tid = None


    def get_req_data(self, *args, **kwargs):
        return get_req_dataset(*args, **kwargs, target=self.target, ri=self.ri, tid=self.tid)

    @task
    def statusNotificationAvailable(self):
        self.target = get_target()
        self.meter = 0
        # print(f'Charger 실행 Client:{len(using_clients)}개')
        # print(f'Charger {using_clients}')

        req_name = "statusNotification"
        self.ri = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}_card"
        req = self.get_req_data(req_name, status="Available")


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
        response = self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        # print(response)
        # print(response.json())

    @task
    def statusNotificationPreparing(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, status="Preparing")
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
        if 'transactionId' in response.json() :
            self.tid = response.json()['transactionId']
        else:
            print(f"No Transaction Id : {response}")

    @task
    def statusNotificationCharging(self):
        req_name = "statusNotification"
        req = self.get_req_data(req_name, status="Charging")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task(10)
    def meterValues(self):
        req_name = "meterValues"
        self.meter += 10
        req = self.get_req_data(req_name, meter=self.meter)
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
        req = self.get_req_data(req_name)
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
        req = self.get_req_data(req_name, status="Finishing")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        remove_target(self.target)


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
    # tasks ={EvTaskSequential:1, EvMobileTaskSequence:1}
    tasks =[EvMobileTaskSequence]
    # tasks =[EvTaskSequential]
    # tasks =[OneServer]
    wait_time = between(0.3,0.5)
