# Her skrives alle krav som stilles til signalet for å få UART-kommunikasjon til å fungere:


1. Må sende en wake up kommando for å få magnetometeret til å gå inn i "operational mode". Dette gjøres ved å sende en positiv flanke på TX-pinnen. "Rising edge signal on the UART - TX pin" Dette er TX på picoen, altså RX på bærekortet. (Pico -> Host)

# Oppfylt?
Hvis det menes TX-pinnen på magnetometeret, så nei.
Hvis ikke, ja. 

# Nåværende implementasjon:
Funksjonen 'uart_wakeup_cmd(serial, wakeup_time)' sender '@' fra TX-pinnen til bærekortet. @ er 01000000 i ascii bit, som dermed blir en positiv flanke. Det er mulig å sende for eksempel '00000010', men den førstnevnte er den første leselige ascii bokstaven med kun ett 1-tall. Funksjonen blir kalt rett etter oppstart av UART-kommunikasjonen

# Fremtidig implementasjon:
Er nødt til å endre koden slik at det sendes en positiv flanke fra bærekortets RX-pinne!!!!
Hvis vi finner ut av at sluttbit-en fungerer som den skal, vil det være mulig å sende '00000000', der sluttbit-en vil skape den positive flanken. Men igjen, hvis '@' funker trenger vi ikke endre noe.


2. Riktig spenningsnivåer på de logiske nivåene på RX/TX pinnene. Disse kan ta spenningsverdier i intervallet [GND-0.5V. VCCIN+0.5V]

# Oppfylt?
Ja. 

# Nåverende implementasjon
Har blitt testet. Det blir sendt et signal som ligger mellom 0V og 3.3V

# Fremtidig implementasjon
Ingenting


3. Riktig kommunikasjonskonfigurasjon. Riktig baudrate, stop/startbit, polaritet og port

# Oppfylt?
Logikk sier ja, men parametrene har ikke blitt verifisert

# Nåværende implementasjon
Vi får ingen feilmelding når vi åpner seriell kommunikasjon, men vi får ingen respons fra magnetometeret. Parametrene har ikke blitt verifisert i pico-en, så dette er en feilkilde

# Fremtidig implementasjon
verifiser alle kommunikasjonsparametre i pico-en


4. Mens systemet booter og går inn i shutdown mode så må UART-RX (Host -> Pico) være HØY

# Oppfylt?
Ja. 
Hvis vi ikke skriver noe til TX pinnen på bærekortet er denne alltid HØY (idle logic level)

# Nåværende implementasjon
Ingen kode, kun det faktum at TX alltid er høy ved mindre den sender data-rammer

# Fremtidig implementasjon
Hvis vi blir desperate etter å få dette til å funke kan vi prøve å verifisere at denne forblir HØY mens systemet booter, men ingen umiddelbare planer
