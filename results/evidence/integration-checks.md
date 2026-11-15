# Integration Check Record

Date: 2026-11-13
Branch: person3-sdn-integration
Code commit tested: 8ef2e9a

## Reservation ID on reserve and release

Request:

    RESERVE|C1|10|120

Server response:

    ACCEPTED|C1|10|bef276cd355a

Request:

    RELEASE|C1

Server response:

    RELEASED|C1|bef276cd355a

The ID in the accepted and released responses matched.

## Automatic expiry cleanup

Request:

    RESERVE|C2|10|5

Server response:

    ACCEPTED|C2|10|fbe660937bfb

After waiting 7 seconds, STATUS returned:

    TOTAL=100|USED=0|AVAILABLE=100

The qdisc check on s1-eth3 returned:

    qdisc noqueue 0: root refcnt 2
    Sent 0 bytes 0 pkt (dropped 0, overlimits 0 requeues 0)
    backlog 0b 0p requeues 0

This confirmed that the reservation expired, capacity was released, and the limiter was removed.

## Code checks

Command:

    python3 -m py_compile p1-socket-reservation/server_integrated.py policy_bridge.py

Result: no output; syntax check passed.

Command:

    git diff --check

Result: no output; whitespace check passed.

## Evidence note

This is a written record of terminal outputs observed during Mininet testing. It is not a raw terminal log or screenshot.
