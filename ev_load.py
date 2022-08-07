'''
    locust -f ev_load.py EvLocus --host https://stgevspcharger.uplus.co.kr

'''
from locust import HttpUser,TaskSet, SequentialTaskSet,between
import json, random, datetime

from locust.user import task

client_size = 50
userIds = [
    'gabardine28@voltup.com','gabbro13@voltup.com',
    'gabbro73@voltup.com','gaberones25@voltup.com',
    'gaberones39@voltup.com','gable53@voltup.com',
    'gable82@voltup.com','gabriel1@voltup.com',
    'gabriel73@voltup.com','gabrielle19@voltup.com',
    'gabrielle23@voltup.com','gabrielle29@voltup.com',
    'gabrielle8@voltup.com','gad41@voltup.com',
    'gad49@voltup.com','gadget48@voltup.com',
    'gadgetry13@voltup.com','gadolinium51@voltup.com',
    'gadwall12@voltup.com','gaff19@voltup.com',
    'gaffe95@voltup.com','gag23@voltup.com',
    'gagging73@voltup.com','gagging90@voltup.com',
    'gagging96@voltup.com','gagwriter56@voltup.com',
    'gaiety7@voltup.com','gail17@voltup.com',
    'gail50@voltup.com','gaillardia26@voltup.com',
    'gaillardia54@voltup.com','gaillardia7@voltup.com',
    'gaillardia81@voltup.com','gain32@voltup.com',
    'gain98@voltup.com','gaines1@voltup.com',
    'gaines48@voltup.com','gainesville5@voltup.com',
    'gainesville88@voltup.com','gait2@voltup.com',
    'gait38@voltup.com','gait94@voltup.com',
    'gaithersburg16@voltup.com','gal83@voltup.com',
    'galactose37@voltup.com','galapagos45@voltup.com',
    'galaxy71@voltup.com','galbreath13@voltup.com',
    'galbreath37@voltup.com','galbreath66@voltup.com',
    ]
userIds = [
    "nheo.an@gmail.com","nheo.an@gmail.com","nheo.an@gmail.com","nheo.an@gmail.com","nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
    "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com", "nheo.an@gmail.com",
]

userPasswords = []

idTags = [
    '4382308400316372',  '4531031214984422',    '4114323326597027',  '4931668367673172',
    '4341266918500034',  '4557495885235197',   '4348505934924235',  '4470140264744450',
    '4929352272953863',  '4583271986891151',    '4889184418649882',  '4292816817194257',
    '4268133858541948',  '4446490404441900',    '4158301215042052',  '4184668486894898',
    '4374178688993554',  '4623338292422792',    '4773215833139973',  '4489797772061579',
    '4674563082552014',  '4180471897477137',    '4128583879499636',  '4858029120594217',
    '4515534185096322',  '4804195102839941',   '4364283845751708',  '4182340583173074',
    '4676711773461796',  '4129568701443620',    '4645924929853346',  '4979632618325522',
    '4443826240981241',  '4816739466121282',    '4224249954086226',  '4681519433089622',
    '4878959395905362',  '4655994839522754',    '4618474608693811',  '4151885532561961',
    '4102840694945284',  '4824843456599063',    '4246993680810312',  '4501713624590205',
    '4804495403291733',  '4338557699462003',    '4488456989794751',  '4572084089788353',
    '4849637386573768',  '4333206210061515',
]

crgrList = [
    '111700001010C', '111700001020C', '111700001030C', '111700001040C',
    '111700001060C', '111700001070C', '111700002010C', '111700002020C',
    '111700002030C', '111700002040C', '111700002050C', '111700002060C',
    '111700002070C', '111700002080C', '111700002090C', '111700003010A',
    '111700003020A', '111700003030A', '111700003040A', '111700003050A',
    '111700003060A', '111700003070A', '111700003080A', '111700003090A',
    '111700004010C', '111700004020C', '111700004030C', '111700004040C',
    '111700004050C', '111700004060C', '111700004070C', '111700004080C',
    '111700004090C', '111700005010A', '111700005020A', '111700005030A',
    '111700005040A', '111700005050A', '111700005060A', '111700005070A',
    '111700005080A', '111700005090A', '111700006010A', '111700006020A',
    '111700006030A', '111700006040A', '111700006050A', '111700006070A',
    '111700006080A', '111700001050C',

]

charger_host = "https://stgevspcharger.uplus.co.kr"
#service_host = "https://devevsp.uplus.co.kr"
service_host = "https://api.stgevsp.uplus.co.kr"
deferred_host = "https://dev"

urls = {
    "authorize":charger_host+"/api/v1/OCPP/authorize/999332",
    "bootNotification":charger_host+"/api/v1/OCPP/bootNotification/999332",
    "heartbeat":charger_host+"/api/v1/OCPP/dataTransfer/999332",
    "prepare":charger_host+"/api/v1/OCPP/statusNotification/999332",
    "tariff":charger_host+"/api/v1/OCPP/dataTransfer/999332",
    "startTransaction":charger_host+"/api/v1/OCPP/startTransaction/999332",
    "stopTransaction":charger_host+"/api/v1/OCPP/stopTransaction/999332",
    "meterValues":charger_host+"/api/v1/OCPP/meterValues/999332",
    "statusNotification": charger_host + "/api/v1/OCPP/statusNotification/999332",

    "validateMemberId": service_host+"/pub-api/v1/MIF/validateMemberId",
    "login": service_host + "/cmm-api/v1/AUTH/login",
    "retrieveChargeStationInfo": service_host + "/pub-api/v1/HMN/retrieveChargeStationInfo",
    "retrieveChargerInfo": service_host + "/pub-api/v1/HMN/retrieveChargerInfo",
    "retrieveDeferredPaymentCardInfo": service_host + "/api/v1/CFN/retrieveDeferredPaymentCardInfo",
    "insertOrder": service_host + "/pub-api/v1/ORDER/insertOrder",
    "updateOrder": service_host + "/pub-api/v1/ORDER/updateOrder",
}
conn = None
client_list = [i for i in range(client_size)]
using_clients = list()

def getConnection():
    import pymysql
    conn = pymysql.connect(host="rds-aurora-mysql-ev-charger-svc-instance-0.cnjsh2ose5fj.ap-northeast-2.rds.amazonaws.com",
                           user='evsp_usr', password='evspuser!!', db='evsp', charset='utf8', port=3306)

def getCards():

    with conn.cursor() as cur:
        cur.execute(" select b.mbr_card_no "+
                    " from mbr_info a "+
                    " inner join mbr_card_isu_info b "+
                    " on a.mbr_id = b.mbr_id "+
                    " where b.card_stus_cd = '01'")
        return cur.fetchall()


def getCrgrs(chrstn_id = None):

    with conn.cursor() as cur:
        sql = " select b.crgr_cid " \
              " from crgr_mstr_info a " \
              " inner join crgr_info b " \
              " on a.crgr_mid = b.crgr_mid " \
              " where a.crgr_stus_cd = '04' and b.crgr_cid like '%A'"

        if chrstn_id :
            sql = sql + f" and a.chrstn_id = '{chrstn_id}' "
        cur.execute(sql)

        return cur.fetchall()

def login():
    import requests
    req = get_req_data("login")
    response = requests.post(urls["login"], headers=req["header"],
                             data=json.dumps(req["body"]))

    # print(response.text)
    # print(response.json())
    #
    # response_dict = response.json()
    #
    # return response_dict["data"]["payload"]["accessToken"]


def get_req_data(req, *args):

    while True:
        target = random.choice(client_list)
        if target not in using_clients :
            break

    using_clients.append(target)

    header = {'Content-type': 'application/json', 'Accept': 'application/json', 'Cache-Control': 'no-cache',
               'Pragma': 'no-cache', 'X-EVC-RI': f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}_card" , 'X-EVC-BOX': crgrList[target],
               'X-EVC-MDL': 'LGE-123', 'X-EVC-OS': 'Linux 5.5'
              }

    if req == "authorize" :
        body = {'idTag': f'{idTags[target]}'}

    elif req == "validateMemberId":
        body = {"mbrId": userIds[target]}
        header = {"Content-Type": "application/json"}
    elif req == "login":
        body = {"userId": userIds[target], "userPw": 'ah64jj3!'}
        header = {"Content-Type": "application/json"}

    elif req == "retrieveChargeStationInfo":
        body = {"chrstnId": crgrList[target][:9]}
    elif req == "retrieveChargerInfo":
        body = {"crgrCid": crgrList[target]}
    elif req == "retrieveDeferredPaymentCardInfo":
        body = {}
    elif req == "insertOrder":
        body = {"reqEtfnQt":40,"reqEtfnAmt":9000,"chrstnId":crgrList[target][:9],"crgrCid":crgrList[target],"ordrDivsCd":"01","etfnUprcAmt":225,"serverFrom":"svc","etfnQt":40,"etfnAmt":9000,"ordrCntnCd":"01"}
    elif req == "updateOrder":
        body = {"ordrNo":args[0],"ordrRsltCd":"03"}

    elif req == "statusNotification":
        body = {'connectorId': '0', 'errorCode': 'NoError', 'info': {'reason': 'None', 'cpv': 100, 'rv': 11},
                'status': args[0], 'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}Z',
                'vendorErrorCode': '', 'vendorId': 'LGE'}
    elif req == "tariff":
        body = {'venderId': 'LG', 'messageId': 'Tariff',
                'data': {'connectorId': '0', 'idTag': idTags[target],
                         'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}'}}
    elif req == "startTransaction":
        body = {'idTag': idTags[target], 'connectorId': '0', 'meterStart': 109065,
                'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}'}
    elif req == "stopTransaction":
        body = {'idTag': idTags[target], 'meterStop': 111136, 'reason': 'Finished',
        'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}', 'transactionId': '202207031120000120005'}
    elif req == "meterValues":
        body = {'connectorId': '0', 'transactionId': args[0],
                'meterValue': [{'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}',
                                'sampledValue': [
                                     {'measurand': 'Energy.Active.Import.Register', 'unit': 'Wh', 'value': '1046.0'},
                                ]}]}

    using_clients.remove(target)

    return {"header":header, "body":body}


class EvMobileTaskSequence(SequentialTaskSet):

    tid = None
    accessToken = None

    # def on_start(self):
    #     accessToken = login()
    #     print(accessToken)

    # @task
    # def validateMemberId(self):
    #     req_name = "validateMemberId"
    #     req = get_req_data(req_name)
    #
    #     response =self.client.post(
    #         url=urls[req_name],
    #         data=json.dumps(req["body"]),
    #         auth=None,
    #         headers=req["header"],
    #         name=req_name,
    #     )
    #     print(response)

    @task
    def login(self):
        req_name = "login"
        req = get_req_data(req_name)

        response =self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        accessToken = response.json()['data']['payload']['accessToken']

    @task
    def retrieveChargeStationInfo(self):
        req_name = "retrieveChargeStationInfo"
        req = get_req_data(req_name)

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
        req = get_req_data(req_name)

        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def retrieveDeferredPaymentCardInfo(self):
        req_name = "retrieveDeferredPaymentCardInfo"
        req = get_req_data(req_name)

        response = self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def insertOrder(self):
        req_name = "insertOrder"
        req = get_req_data(req_name)

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
        req = get_req_data(req_name, self.tid)

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
        req = get_req_data(req_name, "Charging")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )

    @task
    def meterValues(self):
        req_name = "meterValues"
        req = get_req_data(req_name, self.tid)
        response = self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )
        print(req["body"])
        print(response.json())

    @task
    def stopTransaction(self):
        req_name = "stopTransaction"
        req = get_req_data(req_name, self.tid)
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
        req = get_req_data(req_name, "Finishing")
        self.client.post(
            url=urls[req_name],
            data=json.dumps(req["body"]),
            auth=None,
            headers=req["header"],
            name=req_name,
        )


class EvTaskSequential(SequentialTaskSet):

    tid = None
    @task
    def statusNotificationAvailable(self):
        req_name = "statusNotification"
        req = get_req_data(req_name, "Available")

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
        req = get_req_data(req_name)
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
        req = get_req_data(req_name, "Preparing")
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
        req = get_req_data(req_name)
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
        req = get_req_data(req_name)
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
        req = get_req_data(req_name, "Charging")
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
        req = get_req_data(req_name, self.tid)
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
        req = get_req_data(req_name, self.tid)
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
        req = get_req_data(req_name, "Finishing")
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
    tasks ={EvMobileTaskSequence:1, EvTaskSequential:5}

    wait_time = between(0.3,0.5)
