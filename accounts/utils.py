# Natalija
# Provera podataka za registarciju
def  check_data_for_registration(username, birthdate, birthplace, name,surname, phone_number, password, confirm_password, email, card):
    message= ""

    if exists_username(username):
        message+="Korisničko ime "+username+" već postoji!\n"
    else:
        if not valid_username_format(username):
            message += "Korisničko ime nije validnog formata!\n"
    if not valid_birthdate(birthdate):
        message += "Datum rođenja nije validan!\n"
    if not valid_birthplace(birthplace):
        message += "Mesto rođenja nije validno!\n"
    if not valid_name(name):
        message+="Ime nije validno!\n"
    if not valid_surname(surname):
        message+="Prezime nije validno!\n"
    if not valid_phone_number(phone_number):
        message+="Broj telefona nije u validnom formatu!\n"
    if not valid_password(password):
        message+="Šifra ne zadovoljava kriterijume!\n"
    else:
        if password != confirm_password:
            message+="Potvrda šifre i šifra se ne poklapaju!\n"
    if not valid_email(email):
        message+="Mejl adresa nije u dobrom formatu!\n"
    if not valid_card_number(card):
        message+="Broj kartice nije u dobrom formatu!\n"

    return ""



# Provera da l username postoji u tabeli korisnik i tabeli poslatih zahetava za registraciju
def exists_username(username):
    pass

# Provera username formata
def valid_username_format(username):
    pass

def valid_birthdate(birtdate):

    # ako je korisnik mladji od 14 godina, ne prihvataj
    pass
# mozda moze da se zameni sa nekom select formom koja sadrzi sva mesta u svetu npr. samo zemlje
def valid_birthplace(birthplace):
    # ako ne pocinje velikim slovom je lose
    pass

def valid_name(name):
    pass

def valid_surname(surname):
    pass

def valid_phone_number(phone_number):
    pass

def valid_password(password):
    pass

def valid_email(email):
    pass

def valid_card_number(card):
    pass