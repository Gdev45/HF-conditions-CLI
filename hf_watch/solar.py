import requests
import xml.etree.ElementTree as ET


SOLAR_URL = "https://www.hamqsl.com/solarxml.php"


class HFWatch:

    def __init__(self):
        self.sfi = "---"
        self.k = "---"
        self.a = "---"

        self.condition = "WAIT"

        self.bands = {
            "10m": "---",
            "20m": "---",
            "40m": "---",
            "80m": "---",
        }


    def update(self):

        try:
            response = requests.get(
                SOLAR_URL,
                timeout=10,
                headers={
                    "User-Agent": "HF-Watch-CLI"
                }
            )

            response.raise_for_status()

            root = ET.fromstring(response.text)


            self.sfi = root.findtext(
                ".//solarflux",
                "---"
            )

            self.k = root.findtext(
                ".//kindex",
                "---"
            )

            self.a = root.findtext(
                ".//aindex",
                "---"
            )


            self.calculate()


        except Exception as e:
            self.condition = "ERROR"
            print(f"Data error: {e}")



    def calculate(self):

        try:
            s = int(self.sfi)
            k = int(self.k)
            a = int(self.a)

        except ValueError:
            self.condition = "NO DATA"
            return



        score = 0


        # Overall conditions

        if s >= 150:
            score += 2

        elif s >= 100:
            score += 1



        if k <= 2:
            score += 2

        elif k == 3:
            score += 1

        elif k >= 5:
            score -= 2



        if a <= 10:
            score += 1

        elif a > 20:
            score -= 1



        if score >= 4:
            self.condition = "GOOD"

        elif score >= 2:
            self.condition = "FAIR"

        elif score >= 0:
            self.condition = "POOR"

        else:
            self.condition = "BAD"



        # Band predictions

        if s >= 140 and k <= 3:
            self.bands["10m"] = "GOOD"

        elif s >= 100:
            self.bands["10m"] = "FAIR"

        else:
            self.bands["10m"] = "LOW"



        if s >= 100 and k <= 4:
            self.bands["20m"] = "GOOD"

        else:
            self.bands["20m"] = "FAIR"



        if k <= 4:
            self.bands["40m"] = "GOOD"

        else:
            self.bands["40m"] = "LOW"



        if a <= 15:
            self.bands["80m"] = "FAIR"

        else:
            self.bands["80m"] = "LOW"
