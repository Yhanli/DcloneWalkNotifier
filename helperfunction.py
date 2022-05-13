from datetime import datetime


def write(self, *args):
    print(f"\n************ {datetime.now()} ************")
    print(" ".join(s for s in args))
