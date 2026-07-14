import requests
import xml.etree.ElementTree as ET


URL = "https://www.hamqsl.com/solarxml.php"


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

        r = requests.get(URL, timeout=10)
        r.raise_for_status()

        root = ET.fromstring(r.text)

        self.sfi = root.findtext("solarflux", "---")
        self.k = root.findtext("kindex", "---")
        self.a = root.findtext("aindex", "---")

        self.calculate()


    def calculate(self):

        s = int(self.sfi)
        k = int(self.k)
        a = int(self.a)


        score = 0


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



        # bands

        self.bands["10m"] = (
            "GOOD" if s >= 140 and k <= 3
            else "FAIR" if s >= 100
            else "LOW"
        )


        self.bands["20m"] = (
            "GOOD" if s >= 100 and k <= 4
            else "FAIR"
        )


        self.bands["40m"] = (
            "GOOD" if k <= 4
            else "LOW"
        )


        self.bands["80m"] = (
            "FAIR" if a <= 15
            else "LOW"
        )
