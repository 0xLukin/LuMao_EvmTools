from web3 import Web3
import requests
import cfscrape
import json
import time
from dotenv import load_dotenv
load_dotenv()
import os


api_url ='api.bscscan.com'
YOUR_API_KEY = "YGU4ZK9PXZUU786QB5WECN5WKINDNMW8DV"

Main_Address = os.getenv("Main_Address")
Main_Key = os.getenv("Main_Key")

NftContract_Address = "0xa2b2a7774e29f13E17F95b0fc9c0722e7Be36E49" #nft合约地址

NftMatchContract_Address = "0x1Bae64efe6824C84c47f16606e5013CEFcc5a514" #nft分发合约地址，合约之前先将nft全部授权给分发合约
NftMatchContract_Abi = json.loads(
  '[{"inputs":[{"internalType":"address","name":"_nftAddress","type":"address"},{"internalType":"address[]","name":"_add","type":"address[]"},{"internalType":"uint256[]","name":"_id","type":"uint256[]"}],"name":"matchNft","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"stateMutability":"nonpayable","type":"constructor"}]'
)

bsc_url = "https://bsc-dataseed1.binance.org"
web3 = Web3(Web3.HTTPProvider(bsc_url))  # 建立连接


# bnb_balance = web3j.fromWei(int(bnb_balance), "ether")

def gettime():
  return str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

def getNftId(startblock,endblock):
  startblock = startblock

  url = "https://api.bscscan.com/api?module=account&action=tokennfttx&contractaddress="+NftContract_Address+"&address="+Main_Address+"&page=1&offset=100&startblock="+startblock+"&endblock="+endblock+"&sort=desc&apikey="+YOUR_API_KEY

  scraper = cfscrape.create_scraper()
  response = scraper.get(url).content
  res = json.loads(response)['result']
  tokenId=[]
  for re in res:
    print(re)
    tokenId.append(int(re['tokenID']))
  print(len(res))
  print(tokenId)
  return  res

# 批量转移nft
def nftMatch(batch_list,batch_tokenID):

    contract_address = Web3.toChecksumAddress(NftMatchContract_Address)
    nft_address = Web3.toChecksumAddress(NftContract_Address)
    # BatchContract ABI

    main_add = Web3.toChecksumAddress(Main_Address)
    contract = web3.eth.contract(address=contract_address, abi=NftMatchContract_Abi)
    print(contract.all_functions())
    nonce = web3.eth.getTransactionCount(main_add)
    print("nonce:"+str(nonce))
    gas_price = web3.eth.gasPrice

    for i in range(len(batch_list)):
        batch_list[i] = Web3.toChecksumAddress(batch_list[i])
    print(batch_list)

    txn = contract.functions.matchNft(nft_address,batch_list,batch_tokenID).buildTransaction({
        'nonce': nonce,
        'value': web3.toWei(0, 'ether'),
        'gas': 210000,
        'gasPrice': gas_price,
    })

    signed_tx = web3.eth.account.signTransaction(txn, Main_Key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    hash = web3.toHex(tx_hash)
    print(hash)
    return hash

# .env文件配置主账号和私钥

end = 23041409
start = 22924372
res = getNftId(str(start),str(end))
addresses = ["0x542E866778FEA130C183A001B385b7fA69fa2bDD"]
tokenID = [42689]
nftMatch(addresses,tokenID)

