# Example nats.io patterns

## Prepare environment
```
$ cd ./priv/python
$ ./setup.sh
```

## Run tests

### Test request/response

in console A start the server:

```python
# in ipython
import server
server.main()
```

in console B use the client to call a function:

```python
# from ipython
import client
client.make_rpc_call("help", b"joel")
```

you can run the client from bash as follows:

```sh
# from shell
python3 -c "import client; print(client.make_rpc_call('help', b'joel'))"
```




### Test pub/sub

in console A start the consumer:

```python
# in ipython
import consumer
consumer.main()
```

in console B produce a message:

```python
import producer
producer.publish("help.me", "joel")
```

you can run the producer from bash as follows:

```sh
python3 -c "import producer; producer.publish('help.me', 'joel')"
```
