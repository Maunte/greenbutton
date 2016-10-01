Green Button REST Python
========================
Python Client that utilizes the Green Button REST API using Oauth2. It handles authentication and error handling. It can also limit the number of calls made
<br />

Full GreenButton RESTful API documentation - http://energyos.github.io/OpenESPI-GreenButton-API-Documentation/API/

Requirements
========================
* Python 3.5.2
* Flask 0.11.1
* Requests 2.11.1

Usage
========================
```python
from GreenButtonRest.clientV2 import GreenClient
gc = GreenClient()
```
Then use gc.execute(method='') to call the various methods (see documentation below) 

