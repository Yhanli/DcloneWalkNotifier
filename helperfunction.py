from datetime import datetime


def write(*args, **kwargs):
    print(f"\n************ {datetime.now()} ************")
    print(" ".join(str(s) for s in args))
