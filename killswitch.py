#!/usr/bin/python3

import json, requests, subprocess, time;

def get_ip():
    r = requests.get("https://wtfismyip.com/json");
    return json.loads(r.text);

def main():
    TEMPO_SEGUNDOS_AGUARDAR = 30;
    country = ["brazil", "panama"];
    while True:
        try:
            retorno = get_ip();
            if retorno["YourFuckingCountry"].lower() in country:
                subprocess.call(["ip", "route", "del", "default"]);
                print("Parando a Internet, IP do " + retorno["YourFuckingCountry"] + " detectado.");
                TEMPO_SEGUNDOS_AGUARDAR = 0;
                break;
        except:
            print("Continue....");
        finally:
            time.sleep(TEMPO_SEGUNDOS_AGUARDAR);
if __name__ == "__main__":
    main();

