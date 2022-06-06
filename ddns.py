#!/usr/bin/env python
#coding=utf-8
import json
import time
import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest

credentials = AccessKeyCredential('<your-access-key-id>', '<your-access-key-secret>')
client = AcsClient(region_id='<place-your-in>', credential=credentials)


def ddnsmain(ipv6):
    # use STS Token
    # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')


    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')

    request.set_RecordId("762844858256210944")
    request.set_RR("ipv6")
    request.set_Type("AAAA")
    request.set_Value(ipv6)
    try:
        response = client.do_action_with_exception(request)
    except:
        return "False"
    # python2:  print(response) 
    #print(str(response, encoding='utf-8'))
    return response


def getIPv6Address():
    text = requests.get('https://v6.ident.me').text
    return text

def getdnsipv6():

    #credentials = AccessKeyCredential('<your-access-key-id>', '<your-access-key-secret>')
    # use STS Token
    # credentials = StsTokenCredential('<your-access-key-id>', '<your-access-key-secret>', '<your-sts-token>')
    #client = AcsClient(region_id='cn-hangzhou', credential=credentials)

    request = DescribeDomainRecordInfoRequest()
    request.set_accept_format('json')

    request.set_RecordId("762844858256210944")
    try:
        response = client.do_action_with_exception(request)
    except:
        return "False"
    # python2:  print(response) 
    #print(str(response, encoding='utf-8'))
    decode_value=json.loads(response)
    value=decode_value['Value']

    return value




if __name__ == '__main__':
    
    ipv6=getdnsipv6()

    while True:    #永真循环

        t=time.localtime()

        t_s='['+str(t.tm_hour)+':'+str(t.tm_min)+':'+str(t.tm_sec)+']'

        print(t_s+'[I]当前ipv6:'+ipv6)

        nipv6=getIPv6Address()

        if not ipv6==nipv6:

            print(t_s+'[I]将'+ipv6+'修改至'+nipv6)

            if ddnsmain(nipv6)=="False":

                print("\033[31m"+t_s+"[E]DDNS错误\033[0m")

            else:

                print("\033[32m"+t_s+"[I]DDNS成功\033[0m")

                ipv6=nipv6

        else:

            time.sleep(30)#缓冲时间
        