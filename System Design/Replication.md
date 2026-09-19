## Problem with Replication Lag

Leader replication: it requires all the writes to go through a single node, but read-only queries can go to any replica.

[[read-scaling Architecture]] increase the capacity for serving read-only requests simply by adding more followers.