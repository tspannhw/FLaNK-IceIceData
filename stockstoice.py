import pyarrow.parquet as pq
import pyarrow.compute as pc
import pyarrow as pa
from pyiceberg.catalog import load_catalog
from pyarrow import fs
import json
import pandas as pd
from pyarrow import csv
import datetime
import subprocess
import sys
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError
import random
import time
from yahoo_fin import stock_info as si
from yahoo_fin import news  as sn
from yahoo_fin import options as so
from datetime import datetime, timezone
import time
import logging
import sys
import subprocess
import os
import traceback
import math
from time import gmtime, strftime
import random, string
import time
import psutil
import uuid
import requests
from time import sleep
from math import isnan
from subprocess import PIPE, Popen
import socket
import argparse
import os.path
import re
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from time import sleep
from math import isnan
import datetime
import subprocess
import sys
import os
from subprocess import PIPE, Popen
import traceback
import base64
from time import gmtime, strftime
import random, string
import base64
import uuid
import json

StockNames = ["ORCL", "SAP", "CSCO","GOOG","ETH-USD", "NVDA", "AMZN",  "IBM", "NFLX"]
n = 1
producer = KafkaProducer(key_serializer=str.encode, value_serializer=lambda v: json.dumps(v).encode('ascii'),bootstrap_servers='kafka:9092',retries=3)

tablename = "yfinstocks"
schemaname = "docs_example" 
s3location = "s3://pyiceberg"
local_data_dir = "/tmp/stocks/"

from pyiceberg.catalog.sql import SqlCatalog
warehouse_path = "/tmp/warehouse"
catalog = SqlCatalog(
    "docs",
    **{
        "uri": f"sqlite:///{warehouse_path}/pyiceberg_catalog.db",
        "warehouse": "http://localhost:9000",
        "s3.endpoint": "http://localhost:9000",
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": "s3miniokey",
        "s3.secret-access-key": "s3miniosecretkey",
    },
)

rowCounter = 0
isList = []

while rowCounter >= 0:
    stockname = random.choice(StockNames)
    ts = time.time()
    uuid_key = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())
    try:
        row = {'uuid': uuid_key, 'stockname': stockname, 'ts': float(int(ts * 1000)), 'currentts': float(strftime("%Y%m%d%H%M%S",gmtime())), 'stockvalue': float(si.get_live_price(stockname)) }
        producer.send(tablename, key=uuid_key, value=row)
        producer.flush()
    except:
        print("Bad stockname " + stockname)

    print(stockname)
    isList.append(row)
    rowCounter = rowCounter + 1

    if ( rowCounter >= 500):
        rowCounter = 0
        
        ## build PyArrow table from python list
        df = pa.Table.from_pylist(isList)
        #### Write to Apache Iceberg on Minio (S3)
        ### - only create it for new table
        table = None
        try:
            table = catalog.create_table(
                f'{schemaname}.{tablename}',
                schema=df.schema,
                location=s3location,
            )
        except:
            print("Table exists, append " + tablename)    
            table = catalog.load_table(f'{schemaname}.{tablename}')

        ### Write table to Iceberg/Minio
        table.append(df)
        isList = []
        df = None 

    time.sleep(1)
        
producer.close()
