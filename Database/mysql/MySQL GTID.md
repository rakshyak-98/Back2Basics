Global Transaction Identifier is a unique ID assigned to each transaction in MySQL replication.

It allow MySQL replicas to know **exactly which transactions have already been replicated,** without relying only on binary-log file names and positions.

GTID makes replication easier because with GTID you can track the transaction sequence

GTID, it can say "I have already executed transactiosn 1-500. Give me everything after that."

check whether GTID 
