import sys
sys.path.append("..")

def test_client():
    """instructions:

        These tests require an rpc server to handle them

        1. in a different console start the server:
            import server
            server.main()

        2. run this test
    """
    import client
    result = client.make_rpc_call("help", b"i am a bytes-like param obj")
    print(result)
    assert result


def test_producer():
    """instructions:

        These tests require a consumer to receive the published message

        1. in a different console start the server:
            import consumer
            consumer.main()

        2. run this test
    """
    import producer
    producer.publish("hey here's a message for you")
