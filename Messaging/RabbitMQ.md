## Configuration

They will be **loaded in alphabetical order**. A common naming practice uses numerical prefixes in filenames to make it easier to reason about the order, or make sure a "defaults file" is always loaded first, regardless of how many extra files are generated at deployment time:

```bash
# => -r--r--r--  1 rabbitmq  rabbitmq    87B Mar 21 19:50 00-defaults.conf
# => -r--r--r--  1 rabbitmq  rabbitmq   4.6K Mar 21 19:52 10-main.conf
# => -r--r--r--  1 rabbitmq  rabbitmq   1.6K Mar 21 19:52 20-tls.conf
# => -r--r--r--  1 rabbitmq  rabbitmq   1.6K Mar 21 19:52 30-federation.conf
```

## Exchange

- it routes messages to the correct queues based on certain rules, called bindings.

different types of exchanges have different routing strategies

1. Direct exchange : routes messages with a specific routing key to a queue with the same key.
2. Topic exchange : allows more flexible routing based on wildcard patterns in the routing key.
3. Fanout exchange : routes messages to all queues bound to it, regardless of the routing key.

# Bindings

- these are like rules that specifies how messages should be routed from an exchange to queues based on the routing key.