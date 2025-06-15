# Sample User Group Walkthrough

This document demonstrates a typical workflow using the Touchstone email tools.
The accompanying `mock_interactions.py` script simulates the email traffic
without sending real messages.

## Scenario

1. **Alice** creates a new group by submitting a signup form.
2. **Bob** joins Alice's group using the group ID she received.
3. **Carol** signs up without specifying a group ID and is given her own group.
4. Alice and Bob send update emails for their group.
5. The app compiles a report and sends it to the group members.

Running `python mock_interactions.py` prints each email the app would send,
including welcome messages and the monthly report.
