https://django.radif.ru

ри тестировании в режиме интернета на VDS идут вод такие ошибки (логин прописан в конфиге siege):

(myprojectenv) radif@vm224274:~/Django_optimization_tools$ siege -f -i /home/radif/Django_optimization_tools/load_testings/urls.txt -d0 -r5 -c1
** SIEGE 4.0.4
** Preparing 1 concurrent users for battle.
The server is now under siege...[error] A non-recoverable resolution error for 

[error] A non-recoverable resolution error for 

[error] A non-recoverable resolution error for 

[error] A non-recoverable resolution error for 

[error] A non-recoverable resolution error for 


Transactions:                     28 hits
Availability:                  84.85 %
Elapsed time:                   2.80 secs
Data transferred:               0.75 MB
Response time:                  0.10 secs
Transaction rate:              10.00 trans/sec
Throughput:                     0.27 MB/sec
Concurrency:                    1.00
Successful transactions:          28
Failed transactions:               5
Longest transaction:            1.36
Shortest transaction:           0.00

