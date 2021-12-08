# clearml client 


## setup

setup python venv 

```sh
python3 -m venv venv
source venv/bin/activate
```

install deps

```sh
pip install -r requirements.txt
```

setup clear ml
```sh
clearml-init
clearml-agent init
```


## running 

run the clearml agent locally 

```sh
clearml-agent daemon --queue default --foreground
```



