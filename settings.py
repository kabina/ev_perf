import datetime

client_size = 200
charger_host = "http://stgevspcharger.uplus.co.kr"
service_host = "http://api.stgevsp.uplus.co.kr"
deferred_host = "http://dev"

def getConnection():
    import pymysql
    conn = pymysql.connect(host="rds-aurora-mysql-ev-charger-svc-instance-0.cnjsh2ose5fj.ap-northeast-2.rds.amazonaws.com",
                           user='evsp_usr', password='evspuser!!', db='evsp', charset='utf8', port=3306)
    return conn

def getCards():
    conn = getConnection()
    with conn.cursor() as cur:
        cur.execute(" select b.mbr_card_no "+
                    " from mbr_info a "+
                    " inner join mbr_card_isu_info b "+
                    " on a.mbr_id = b.mbr_id "+
                    f" where b.card_stus_cd = '01' and b.grp_card_yn = 'N' and b.mbr_card_no like '4%' "
                    f" and a.mbr_id like '%voltup.com' limit {client_size}")
        fetches = cur.fetchall()
        with open('dataset/idTags', 'w') as f:
            for i in fetches:
                f.write(f'{i[0]}\n')

        return [i[0] for i in fetches]

def getUserIds():
    conn = getConnection()
    with conn.cursor() as cur:
        cur.execute(" select mbr_id "+
                    " from mbr_info a "+
                    f" where a.mbr_stus_cd = '01' and a.mbr_id like 'k%' "
                    f" and a.mbr_id like '%voltup.com' limit {client_size}")
        fetches = cur.fetchall()
        with open('dataset/UserIds', 'w') as f:
            for i in fetches:
                f.write(f'{i[0]}\n')

        return [i[0] for i in fetches]

def getCrgrs(chrstn_id = None):

    conn = getConnection()
    with conn.cursor() as cur:
        sql = " select b.crgr_cid " \
              " from crgr_mstr_info a " \
              " inner join crgr_info b " \
              " on a.crgr_mid = b.crgr_mid " \
              f" where a.crgr_stus_cd = '04' and b.crgr_cid like '1117%' limit {client_size}"

        if chrstn_id :
            sql = sql + f" and a.chrstn_id = '{chrstn_id}' "
        cur.execute(sql)

        fetches = cur.fetchall()
        with open('dataset/crgrList', 'w') as f:
            for i in fetches:
                f.write(f'{i[0]}\n')

        return [i[0] for i in fetches]


idTags = getCards()
crgrList = getCrgrs()
userIds = getUserIds()
userPasswords = ['qwer1234!' for i in range(client_size)]


def get_req_dataset(req, *args, **kwargs):
    target = kwargs["target"]

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
        body = {"userId": userIds[target], "userPw": userPasswords[target]}
        header = {"Content-Type": "application/json"}
    elif req == "retrieveChargeStationInfo":
        body = {"lat": 37.5100152, "lon": 126.8393359, "latFrom": 37.4596282, "latTo": 37.5604022, "lonFrom": 126.8031889,
                "lonTo": 126.8754829, "limit": 1, "isFrscChrStn": "Y", "mbrId": f"{idTags[target]}"}
    elif req == "retrieveChargerInfo":
        body = {"crgrCid": crgrList[target]}
    elif req == "retrieveDeferredPaymentCardInfo":
        body = {}
    elif req == "insertOrder":
        body = {"reqEtfnQt":40,"reqEtfnAmt":9000,"chrstnId":crgrList[target][:9],"crgrCid":crgrList[target],
                "ordrDivsCd":"01","etfnUprcAmt":225,"serverFrom":"svc","etfnQt":40,"etfnAmt":9000,"ordrCntnCd":"01"}
        header["authorization"] = f'Bearer {args[0]}'
    elif req == "updateOrder":
        body = {"ordrNo":args[0],"ordrRsltCd":"03"}

    elif req == "sendStartChargeStatus":
        body = {"ordrNo":args[0]}

    elif req == "statusNotification":
        body = {'connectorId': '0', 'errorCode': 'NoError', 'info': {'reason': 'None', 'cpv': 100, 'rv': 11},
                'status': args[0], 'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}Z',
                'vendorErrorCode': '', 'vendorId': 'LGE'}
    elif req == "tariff":
        body = {'venderId': 'LG', 'messageId': 'Tariff',
                'data': {'connectorId': '0', 'idTag': idTags[target],
                         'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}Z'}}
    elif req == "startTransaction":
        body = {'idTag': idTags[target], 'connectorId': '0', 'meterStart': 1000,
                'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}Z', 'reservationId':args[0]}
    elif req == "heartbeat":
        body = {"vendorId":"LGE", "messageId":"heartbeat",
                "data":{"rssi":80,"snr":57, "rsrp":70 }}
    elif req == "stopTransaction":
        body = {'idTag': idTags[target], 'meterStop': 2000, 'reason': 'Finished',
                'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}Z', 'transactionId': args[0]}
    elif req == "meterValues":
        body = {'connectorId': '0', 'transactionId': args[0],
                'meterValue': [{'timestamp': f'{datetime.datetime.now().replace(microsecond=0).isoformat()}Z',
                                'sampledValue': [
                                     {'measurand': 'Energy.Active.Import.Register', 'unit': 'Wh', 'value': 1000+args[1]},
                                ]}]}
    elif req == "retrieveChargingValues":
        body = {'ordrNo': args[1], 'mbrId':userIds[target]}
        header["Authorization"] = f'Bearer {args[0]}'

    return {"header":header, "body":body}


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
    "sendStartChargeStatus": service_host + "/pub-api/v1/HMN/sendStartChargeStatus",
    "retrieveChargingValues": service_host + "/api/v1/HMN/retrieveChargingValues",
}