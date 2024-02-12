import time  # Importerer time modulen for å bruke sleep funksjonen

streng = "Hei"

for bokstav in streng:
    print(bokstav, end='', flush=True)  # Skriver ut hver bokstav uten linjeskift, og sikrer umiddelbar utskrift
    time.sleep(0.1)  # Venter i 0.01 sekunder før neste bokstav skrives ut
