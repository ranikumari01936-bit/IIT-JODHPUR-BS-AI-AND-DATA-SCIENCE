"""
Task 2 - Validation-Based (Optimistic) Concurrency Control
Three-phase state machine per transaction:
    READ/EXECUTION -> VALIDATION -> WRITE   (or ABORTED if validation fails)

Timestamps:
    Start-TS      : assigned when the Read/Execution phase begins
    Validation-TS : assigned when the Validation phase begins
                    -> this is the ONLY timestamp that defines the serial order
    Finish-TS     : assigned when the Write phase ends (commit) or on abort

Validation test for Tj against every Ti with Validation-TS(Ti) < Validation-TS(Tj):
    (a) Finish-TS(Ti) < Start-TS(Tj)                                   OR
    (b) WriteSet(Ti) ∩ ReadSet(Tj) = {}  AND  Finish-TS(Ti) < Validation-TS(Tj)
    If neither holds, Tj fails validation and is rolled back.
"""
import csv
from enum import Enum


class Phase(Enum):
    READ = "READ/EXECUTION"
    VALIDATION = "VALIDATION"
    WRITE = "WRITE"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"


class Database:
    def __init__(self, data):
        self.data = dict(data)


class Transaction:
    def __init__(self, tid, read_items, writes):
        self.tid = tid
        self.read_items = read_items          # items to read
        self.writes = writes                  # {item: new value}, applied only after validation
        self.read_set, self.write_set = set(), set()
        self.local = {}                       # private workspace (not visible to others)
        self.phase = None
        self.start_ts = self.validation_ts = self.finish_ts = None
        self.fail_reason = ""


class Scheduler:
    def __init__(self, db):
        self.db = db
        self.clock = 0
        self.txns = {}
        self.log = []

    def tick(self):
        self.clock += 1
        return self.clock

    def say(self, msg):
        line = f"[t={self.clock:>2}] {msg}"
        self.log.append(line)
        print(line)

    # ---- Phase 1: Read / Execution ----
    def begin(self, txn):
        txn.start_ts = self.tick()
        txn.phase = Phase.READ
        self.txns[txn.tid] = txn
        for item in txn.read_items:                       # reads come from the committed DB
            txn.read_set.add(item)
            txn.local[item] = self.db.data[item]
        for item, val in txn.writes.items():              # writes go to the LOCAL copy only
            txn.write_set.add(item)
            txn.local[item] = val
        self.say(f"{txn.tid} START-TS={txn.start_ts}  phase={txn.phase.value}  "
                 f"ReadSet={sorted(txn.read_set)} WriteSet={sorted(txn.write_set)} (writes kept local)")

    # ---- Phase 2: Validation ----
    def validate(self, txn):
        txn.validation_ts = self.tick()
        txn.phase = Phase.VALIDATION
        self.say(f"{txn.tid} VALIDATION-TS={txn.validation_ts}  phase={txn.phase.value}")
        for ti in self.txns.values():
            if ti is txn or ti.validation_ts is None or ti.validation_ts >= txn.validation_ts:
                continue
            if ti.phase == Phase.ABORTED:
                continue
            cond_a = ti.finish_ts is not None and ti.finish_ts < txn.start_ts
            overlap = ti.write_set & txn.read_set
            cond_b = (not overlap) and ti.finish_ts is not None and ti.finish_ts < txn.validation_ts
            if cond_a or cond_b:
                self.say(f"    check vs {ti.tid}: OK ({'finished before start' if cond_a else 'no read/write overlap and finished before validation'})")
                continue
            txn.phase = Phase.ABORTED
            txn.finish_ts = self.tick()
            txn.fail_reason = (f"WriteSet({ti.tid})={sorted(ti.write_set)} intersects ReadSet({txn.tid})="
                               f"{sorted(txn.read_set)} on {sorted(overlap)}; Finish-TS({ti.tid})={ti.finish_ts} "
                               f"is not < Start-TS({txn.tid})={txn.start_ts}")
            self.say(f"    check vs {ti.tid}: FAIL -> {txn.fail_reason}")
            self.say(f"{txn.tid} ABORTED (rolled back, nothing written to DB) FINISH-TS={txn.finish_ts}")
            return False
        return True

    # ---- Phase 3: Write ----
    def write(self, txn):
        txn.phase = Phase.WRITE
        for item in txn.write_set:
            self.db.data[item] = txn.local[item]          # first and only time DB is modified
        txn.finish_ts = self.tick()
        txn.phase = Phase.COMMITTED
        self.say(f"{txn.tid} WRITE phase done, COMMITTED  FINISH-TS={txn.finish_ts}  DB={self.db.data}")

    def finish(self, txn):
        if self.validate(txn):
            self.write(txn)


def main():
    db = Database({"A": 100, "B": 200, "C": 300, "D": 400, "E": 500})
    s = Scheduler(db)
    T1 = Transaction("T1", ["A", "B"], {"A": 111})
    T2 = Transaction("T2", ["B", "C"], {"C": 333})
    T3 = Transaction("T3", ["A", "D"], {"D": 444})   # reads A, which T1 overwrites
    T4 = Transaction("T4", ["D", "E"], {"E": 555})

    print("VALIDATION-BASED PROTOCOL - EXECUTION LOG")
    print("=" * 100)
    print(f"Initial DB: {db.data}\n")
    # Concurrent execution: all four start (read phase) in order T1,T2,T3,T4
    for t in (T1, T2, T3, T4):
        s.begin(t)
    # But they VALIDATE in a different order: T2, T1, T3, T4
    for t in (T2, T1, T3, T4):
        s.finish(t)

    order = sorted(s.txns.values(), key=lambda t: t.validation_ts)
    print("\n" + "=" * 100)
    print("Serialization order (by VALIDATION-TS, not START-TS):")
    for t in order:
        print(f"  {t.tid}: Start-TS={t.start_ts}  Validation-TS={t.validation_ts}  "
              f"Finish-TS={t.finish_ts}  -> {t.phase.value}")
    print(f"Start-TS order      : {[t.tid for t in sorted(s.txns.values(), key=lambda t: t.start_ts)]}")
    print(f"Validation-TS order : {[t.tid for t in order]}")
    print(f"Final DB: {db.data}")

    with open("transaction_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Transaction", "Start-TS", "Validation-TS", "Finish-TS", "Read-Set", "Write-Set", "Status"])
        for t in order:
            w.writerow([t.tid, t.start_ts, t.validation_ts, t.finish_ts,
                        " ".join(sorted(t.read_set)), " ".join(sorted(t.write_set)), t.phase.value])
    with open("validation_log.txt", "w") as f:
        f.write("\n".join(s.log) + f"\n\nFinal DB: {db.data}\n")

    return s, T3


if __name__ == "__main__":
    main()
