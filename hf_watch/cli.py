import time
import argparse

from .solar import HFWatch



def display(hf):

    print()
    print("====================")
    print("     HF WATCH")
    print("====================")

    print()
    print("STATUS")
    print("--------------------")

    print(f"SFI: {hf.sfi}")
    print(f"K:   {hf.k}")
    print(f"A:   {hf.a}")

    print()
    print(f"CONDITION: {hf.condition}")

    print()
    print("BANDS")
    print("--------------------")

    for band, status in hf.bands.items():
        print(f"{band:<4} {status}")

    print()



def main():

    parser = argparse.ArgumentParser(
        description="HF propagation monitor"
    )

    parser.add_argument(
        "-w",
        "--watch",
        action="store_true",
        help="refresh every 10 minutes"
    )

    args = parser.parse_args()


    hf = HFWatch()


    while True:

        try:
            hf.update()
            display(hf)

        except Exception as e:
            print("ERROR:", e)


        if not args.watch:
            break


        time.sleep(600)



if __name__ == "__main__":
    main()
