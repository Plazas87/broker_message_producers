from datetime import datetime
import random
import pandas as pd
import time

def main():
    data = {}
    temps = []
    timestamps = []

    for _ in range(1000):
        temps.append(random.randint(10, 40))
        time.sleep(1)
        timestamps.append(str(datetime.now()))

    data["temperature"] = temps
    data["timestamp"] = timestamps

    df = pd.DataFrame(data)

    df.to_csv("./data/room_1/temperature.csv", sep=",", index=False)


if __name__ == "__main__":
    main()