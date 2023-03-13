Hi! Thank you for taking the time to review this!

Please note that this was developed against python 3.10.10 with no regard for health, safety,
or backwards compatibility. Furthermore, this api was developed within WSL2 on Windows 11,
so please make note of any olfactory haunting you may experience. 
See ```https://en.wikipedia.org/wiki/Undefined_behavior``` for context.

From a python virtual environment, in the root directory please run:

```
pip install -r requirements.txt
```

to install the api's dependencies and then run:

```
uvicorn --app-dir=part1 main:app --reload
```

to run the api. 

In your browser, please navigate to ```127.0.0.1:8000/``` to confirm that the api is healthy.
Navigating to ```127.0.0.1:8000/countywinners``` will show primary winners as taken from a 
bastardized version of the sample data provided in the test prompt.

Please forward any questions, concerns, complaints, or heartfelt praise to ```rio.h.kurz@gmail.com```.