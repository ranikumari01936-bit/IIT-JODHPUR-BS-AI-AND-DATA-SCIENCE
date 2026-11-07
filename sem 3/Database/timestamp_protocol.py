"""
Task 1 - Timestamp-Based Concurrency Control (Basic TO protocol)
Data item Q carries two timestamps:
    R-TS(Q) = largest TS of any transaction that read Q successfully
    W-TS(Q) = largest TS of any transaction that wrote Q successfully
"""

class DataItem:
    def __init__(self, name):
        self.name = name
        self.r_ts = 0
        self.w_ts = 0

    def state(self):
        return f"R-TS({self.name})={self.r_ts}, W-TS({self.name})={self.w_ts}"


def read(txn, ts, item):
    """Read(T,Q): reject if TS(T) < W-TS(Q); else grant, R-TS = max(R-TS, TS(T))."""
    if ts < item.w_ts:
        return ("REJECT / ROLLBACK",
                f"TS({txn})={ts} < W-TS({item.name})={item.w_ts}: Q was already overwritten by a younger txn")
    item.r_ts = max(item.r_ts, ts)
    return ("GRANT", f"TS({txn})={ts} >= W-TS={item.w_ts}; R-TS updated to max(R-TS, {ts}) = {item.r_ts}")


def write(txn, ts, item):
    """Write(T,Q): reject if TS(T) < R-TS(Q) or TS(T) < W-TS(Q); else grant, W-TS = TS(T)."""
    if ts < item.r_ts:
        return ("REJECT / ROLLBACK",
                f"TS({txn})={ts} < R-TS({item.name})={item.r_ts}: a younger txn already read Q")
    if ts < item.w_ts:
        return ("REJECT / ROLLBACK",
                f"TS({txn})={ts} < W-TS({item.name})={item.w_ts}: a younger txn already wrote Q")
    item.w_ts = ts
    return ("GRANT", f"TS({txn})={ts} >= R-TS and >= W-TS; W-TS set to {ts}")


DATASET = [  # (seq, txn, ts, op, item)
    (1, "T1", 10, "Read",  "Q"),
    (2, "T2", 20, "Write", "Q"),
    (3, "T3", 15, "Read",  "Q"),
    (4, "T4", 25, "Write", "Q"),
    (5, "T5", 18, "Write", "Q"),
]


def main():
    Q = DataItem("Q")
    lines = []
    def out(s=""):
        print(s)
        lines.append(s)

    out("TIMESTAMP-BASED PROTOCOL - EXECUTION LOG")
    out("=" * 78)
    out(f"Initial state: {Q.state()}")
    out("=" * 78)
    for seq, txn, ts, op, _ in DATASET:
        before = Q.state()
        decision, reason = read(txn, ts, Q) if op == "Read" else write(txn, ts, Q)
        out(f"[{seq}] {op}({txn}, Q)  TS={ts}")
        out(f"     Before  : {before}")
        out(f"     Decision: {decision}")
        out(f"     Reason  : {reason}")
        out(f"     After   : {Q.state()}")
        if decision != "GRANT":
            out(f"     ACTION  : {txn} rolled back; restarts later with a NEW (larger) timestamp")
        out("-" * 78)
    out(f"Final state: {Q.state()}")

    with open("protocol_results.txt", "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
