import os
from datetime import timezone, date

from MySQLdb import IntegrityError, Date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from pyexpat.errors import messages

from Nft_Project import settings
from common.decoraters import is_admin, is_not_admin, is_not_logged_in, is_logged_in
from .utils import check_data_for_registration
# Create your views here.
from .models import Zahtevzaregistraciju, Korisnik, CustomUserManager
from profiles.models import Registrovanikorisnik, Kupac, Kreator, Kolekcionar
from exhibitions.models import Listanft, Kolekcija, Portfolio
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from exhibitions.models import Pripada




#Natalija - logout

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('error')

#Natalija - logovanje na sistem
@user_passes_test(is_not_logged_in,  login_url='/accounts/error')
def login_page(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']


        user= authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Preusmeri korisnika na početnu stranicu nakon uspešnog logina
        else:
            messages.error(request, 'Uneli ste pogrešne kredencijale!')

            return render(request, 'login.html',{})

    return render(request, 'login.html')



# Natalija
# Registracija - prikaz stranice za registraciju i pravljenje zahteva za registraciju
@user_passes_test(is_not_logged_in,  login_url='/accounts/error')
def register_page(request):

    if request.method == 'POST':
        try:
        # Submit dugme je pritisnuto : 1. Povuci podatke iz forme 2. Proveriti podatke iz forme 3.Poslati zahtev za registraciju ukoliko su validni
            username = request.POST['username']
            birthdate = request.POST['birthdate']
            birthplace= request.POST['birthplace']
            first_name = request.POST['name']
            last_name = request.POST['surname']
            phone_number = request.POST['phone']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
            email = request.POST['email']
            card= request.POST['card']
            user_type = request.POST['user_type']
            message = check_data_for_registration(username,birthdate, birthplace,first_name,last_name, phone_number, password, confirm_password, email, card)
            if message=="":
                new_request = Zahtevzaregistraciju(korime=username, ime= first_name, prezime=last_name, sifra=password,
                                                       email= email, brojtelefona=phone_number, brojkartice=card,
                                                       datumrodjenja=birthdate, mestorodjenja=birthplace, uloga=user_type)

                new_request.save()
                return redirect('index')

        except IntegrityError as e:
             message = "Greška pri unosu u bazu: " + str(e)
        return render(request, 'signin.html', {'error': message})

    return render(request, 'signin.html')


#Natalija
#Odobravanje zahteva - brisanje iz baze zahtevi, ukoliko je prijavljen pravljenje novog Korisnika
@login_required( login_url='/accounts/error')
@user_passes_test(is_admin, login_url='/accounts/error')
def registration_request(request):
    if request.method == 'POST':
        #for key, value in request.POST.items():

        all_keys = list(request.POST.keys())  # Pretvaranje ključeva u listu
        action= ""
        id= ""
        if len(all_keys) > 1:
            second_key = all_keys[1]
            action, id= second_key.split('-')

        if action == 'accept':
            request_to_accept = Zahtevzaregistraciju.objects.get(idzah=id)
            # Implementirajte logiku za stvaranje korisnika s podacima iz request_to_accept objekta
            # pravljenje korisnika- pa onda Regsitrovanog pa onda tip

            user= Korisnik(username=request_to_accept.korime, user_type=request_to_accept.uloga)
            user.set_password(request_to_accept.sifra)
            user.save()


            reg_user=  Registrovanikorisnik(ime=request_to_accept.ime,
                                            prezime=request_to_accept.prezime, brojkartice=request_to_accept.brojkartice,
                                            brojtelefona=request_to_accept.brojtelefona, datumrodjenja=request_to_accept.datumrodjenja,
                                            mestorodjenja=request_to_accept.mestorodjenja, email=request_to_accept.email, idkor=user,   datumkreiranja=date.today())



            reg_user.save()

            collection_list = Listanft(idvla=reg_user, ukupnavrednost=0, brojnft=0)
            collection_list.save()

            # Креирање и чување новог Kolekcija објекта
            collection = Kolekcija(idlis=collection_list)
            collection.save()

            image_path = os.path.join(settings.BASE_DIR, 'static/images/def_profile.png')
            with open(image_path, 'rb') as f:
                slika = File(f)
                # Postavljanje slike korisniku
                reg_user.slika.save('def_profile.jpg', slika, save=True)

            if  request_to_accept.uloga=="kreator":
                role= Kreator(idkor=reg_user)
                role.save()
                portfolio_list = Listanft(idvla=reg_user, ukupnavrednost=0, brojnft=0)
                portfolio_list.save()

                # Креирање и чување новог Kolekcija објекта
                portfolio = Portfolio(idlis=portfolio_list)
                portfolio.save()

            elif request_to_accept.uloga=="kupac":
                role = Kupac(idkor=reg_user)
                role.save()
            elif request_to_accept.uloga=="kolekcionar":
                role = Kolekcionar(idkor=reg_user)
                role.save()
            request_to_accept.delete()

        elif action == 'reject':
            # Logika za jednostavno brisanje zahtjeva
            Zahtevzaregistraciju.objects.filter(idzah=id).delete()

    requests = Zahtevzaregistraciju.objects.all()

    return render(request, 'registration_request.html', {'zahtevi': requests})

@login_required( login_url='/accounts/error')
@user_passes_test(is_admin, login_url='/accounts/error')
def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        user = Korisnik.objects.get(username=username)

        reg_user = Registrovanikorisnik.objects.get(idkor=user)

        lists = Listanft.objects.filter(idvla=reg_user)

        # Brisanje objekta pripada za sve liste ciji je korisnik bio vlasnik
        for l in lists:
            for b in Pripada.objects.filter(idlis=l):
                b.delete()

        lists.delete()



        user.delete()

        return redirect("reg_requests")

    else:
        return redirect("error")



@login_required( login_url='/accounts/error')
@user_passes_test(is_not_admin, login_url='/accounts/error')
def change_password(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST['stara-lozinka']
        new_password = request.POST['nova-lozinka']
        confirm_password = request.POST['potvrda-lozinke']

        if not check_password(old_password, user.password):
            messages.error(request, 'Stara lozinka nije ispravna!')

        elif new_password != confirm_password:
            messages.error(request, 'Lozinke se ne podudaraju. Molimo Vas unesite istu lozinku u oba polja!')

        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Lozinka je uspešno promenjena!')
        return render(request, 'change_password.html',{})

    return render(request, 'change_password.html')

def error_view(request):
    error_code='403'
    error_message='permission denied'
    return render(request, 'error.html', {'error_code': error_code, 'error_message': error_message})