from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

from accounts.models import Korisnik
from common.decoraters import is_not_admin
from exhibitions.models import Listanft, Pripada,Izlozba
from nft.models import Nft
from nft.views import get_nft_data
from profiles.models import Registrovanikorisnik
from profiles.utils import create_main_context
from django.contrib import messages


# Create your views here.

#Natalija
# prikaz informacija o profilu, preko searcja, preko buttona moj ptofil- to je else deo - get zahtev
def view_profile_info(request):
    if request.method == 'POST':

        if 'username' in request.POST:

            username = request.POST.get('username', None)
            if username:
                if Korisnik.objects.filter(username=username).exclude(user_type='admin').exists():
                    context = create_main_context(request, username)
                    return render(request, 'profile_info.html', context)
                else:
                    return render(request, "index.html", {"message": True})

        else:
            context = create_main_context(request, request.user.username)

            card = str(Registrovanikorisnik.objects.get(idkor=request.user).brojkartice)
            last_3_digits = card[-3:]
            new_card_view = '*' * (len(card) - 3) + last_3_digits
            context['phone']= Registrovanikorisnik.objects.get(idkor=request.user).brojtelefona
            context['card']= new_card_view
            context['name']= Registrovanikorisnik.objects.get(idkor=request.user).ime
            context['surname']= Registrovanikorisnik.objects.get(idkor=request.user).prezime
            context['birthplace']= Registrovanikorisnik.objects.get(idkor=request.user).mestorodjenja
            return render(request, 'profile_info.html', context)

    else:
        # deo za search treba staviti
        # Ukoliko nije POST zahtev, možemo prikazati formu za unos korisničkog imena ili redirectovati na drugu stranicu
        return HttpResponseNotAllowed(['POST'])




def view_profile_portfolio(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        if username:
            if Korisnik.objects.filter(username=username).exclude(user_type='admin').exists():
                context = create_main_context(request, username)
                #  dopuniti kontekst ya informacije
                id = context["id"]
                listanft = Listanft.objects.filter(portfolio__isnull=False,idvla= id).first()

                pripada_ids = Pripada.objects.filter(idlis=listanft.idlis).values_list('idnft', flat=True)

                nfts = Nft.objects.filter(idnft__in=pripada_ids)

                nft_list = []
                cena = 0
                for nft in nfts:
                    nft_data = {
                        'nft': nft,
                        'data': None
                    }
                    if nft.slika == "":
                        nft_data['data'] = get_nft_data(nft.url)
                    nft_list.append(nft_data)
                    cena += nft.vrednost
                context["nfts"] = nft_list
                context["cena"] = cena
                return render(request, 'profile_portfolio.html', context)
        else:
            return HttpResponse("Molimo vas da unesete korisničko ime.")
    else:
        # deo za search treba staviti
        # Ukoliko nije POST zahtev, možemo prikazati formu za unos korisničkog imena ili redirectovati na drugu stranicu
        return HttpResponseNotAllowed(['POST'])




def view_profile_collection(request):
    if request.method == 'POST':

        username = request.POST.get('username', None)

        if username:
            if Korisnik.objects.filter(username=username).exclude(user_type='admin').exists():
                context = create_main_context(request, username)
                #  dopuniti kontekst ya informacije
                id = context["id"]

                nfts = Nft.objects.filter(idvla=id)

                nft_list = []
                cena = 0
                for nft in nfts:
                    nft_data = {
                        'nft': nft,
                        'data': None
                    }
                    if nft.slika == "":
                        nft_data['data'] = get_nft_data(nft.url)
                    nft_list.append(nft_data)
                    cena += nft.vrednost
                context["nfts"] = nft_list
                context["cena"] = cena
                #context2 = {"nfts": nft_list,"image":context[]}
                return render(request, 'profile_collection.html', context)
        else:
            return HttpResponse("Molimo vas da unesete korisničko ime.")
    else:
        # deo za search treba staviti
        # Ukoliko nije POST zahtev, možemo prikazati formu za unos korisničkog imena ili redirectovati na drugu stranicu
        return HttpResponseNotAllowed(['POST'])
def view_profile_exhibitions(request):
    if request.method == 'POST':

        username = request.POST.get('username', None)

        if username:
            if Korisnik.objects.filter(username=username).exclude(user_type='admin').exists():
                context = create_main_context(request, username)
                id = context["id"]
                listanfts = Listanft.objects.filter(izlozba__isnull=False, idvla=id)

                izlozbe = []
                for listanft in listanfts:
                    nft_list = []
                    pripada_ids = Pripada.objects.filter(idlis=listanft.idlis).values_list('idnft', flat=True)
                    izloz = Izlozba.objects.get(idlis =listanft.idlis)

                    nfts = Nft.objects.filter(idnft__in=pripada_ids)
                    cena = 0
                    for nft in nfts:

                        nft_data = {
                            'nft': nft,
                            'data': None
                        }
                        if nft.slika == "":

                            nft_data['data'] = get_nft_data(nft.url)
                        nft_list.append(nft_data)
                        cena += nft.vrednost
                    izlozba = {
                        'id': izloz.idlis.idlis,
                        'nfts':nft_list,
                        'cena':cena,
                        'naziv':izloz.naziv
                    }
                    izlozbe.append(izlozba)

                context["izlozbe"] = izlozbe

                return render(request, 'profile_exhibitions.html', context)
        else:
            return HttpResponse("Molimo vas da unesete korisničko ime.")
    else:
        # deo za search treba staviti
        # Ukoliko nije POST zahtev, možemo prikazati formu za unos korisničkog imena ili redirectovati na drugu stranicu
        return HttpResponseNotAllowed(['POST'])


def sort_profile_collection(request):
    if request.method == 'POST':

        username = request.POST.get('username', None)

        if username:
            if Korisnik.objects.filter(username=username).exclude(user_type='admin').exists():
                context = create_main_context(request, username)
                #  dopuniti kontekst ya informacije
                sort = request.POST.get('sort', None)
                id = context["id"]
                nfts = Nft.objects.filter(idvla=id)
                nft_list = []
                cena = request.POST.get('cena', None)
                if (sort == "poImenu"):

                    nfts = sorted(nfts, key=lambda nft: nft.naziv)
                elif (sort == "poOceni"):
                    nfts = sorted(nfts, key=lambda nft: nft.prosecnaocena)
                elif (sort == "poVelicini"):
                    pass
                elif (sort == "poVrednosti"):
                    nfts = sorted(nfts, key=lambda nft: nft.vrednost)
                for nft in nfts:

                    nft_data = {
                        'nft': nft,
                        'data': None
                    }
                    if nft.slika == "":
                        nft_data['data'] = get_nft_data(nft.url)
                    nft_list.append(nft_data)
                context["nfts"] = nft_list
                context["cena"] = cena
                pageType = request.POST.get('pageType', None)
                if pageType == "collection":
                  return render(request, 'profile_collection.html', context)
                else:
                  return render(request, 'profile_portfolio.html', context)
        else:
            return HttpResponse("Molimo vas da unesete korisničko ime.")
    else:
        # deo za search treba staviti
        # Ukoliko nije POST zahtev, možemo prikazati formu za unos korisničkog imena ili redirectovati na drugu stranicu
        return HttpResponseNotAllowed(['POST'])

def sort_profile_exhibition(request):
    if request.method == 'POST':

        username = request.POST.get('username', None)

        if username:
            if Korisnik.objects.filter(username=username).exclude(user_type='admin').exists():
                context = create_main_context(request, username)
                #  dopuniti kontekst ya informacije

                sort = request.POST.get('sort', None)
                id = context["id"]
                listanfts = Listanft.objects.filter(izlozba__isnull=False, idvla=id)

                izlozbe = []
                for listanft in listanfts:
                    nft_list = []
                    pripada_ids = Pripada.objects.filter(idlis=listanft.idlis).values_list('idnft', flat=True)
                    izloz = Izlozba.objects.get(idlis=listanft.idlis)

                    nfts = Nft.objects.filter(idnft__in=pripada_ids)
                    cena = 0
                    velicina = 0
                    ocena = 0
                    for nft in nfts:

                        nft_data = {
                            'nft': nft,
                            'data': None
                        }
                        if nft.slika == "":
                            nft_data['data'] = get_nft_data(nft.url)
                        nft_list.append(nft_data)
                        cena += nft.vrednost
                        velicina += 1
                        if nft.prosecnaocena:
                            ocena += nft.prosecnaocena
                    prosOc = float(ocena) / velicina
                    izlozba = {
                        'id': izloz.idlis.idlis,
                        'nfts': nft_list,
                        'cena': cena,
                        'naziv': izloz.naziv,
                        'velicina':velicina,
                        'prosecnaOcena':prosOc
                    }
                    izlozbe.append(izlozba)

                if (sort == "poImenu"):

                    izlozbe = sorted(izlozbe, key=lambda izlozba: izlozba["naziv"])
                elif (sort == "poOceni"):
                    izlozbe = sorted(izlozbe, key=lambda izlozba: izlozba["prosecnaOcena"])
                elif (sort == "poVelicini"):
                    izlozbe = sorted(izlozbe, key=lambda izlozba: izlozba["velicina"])
                elif (sort == "poVrednosti"):
                    izlozbe= sorted(izlozbe, key=lambda izlozba: izlozba["cena"])
                context["izlozbe"] = izlozbe
                return render(request, 'profile_exhibitions.html', context)
        else:
            return HttpResponse("Molimo vas da unesete korisničko ime.")
    else:
        # deo za search treba staviti
        # Ukoliko nije POST zahtev, možemo prikazati formu za unos korisničkog imena ili redirectovati na drugu stranicu
        return HttpResponseNotAllowed(['POST'])


@login_required( login_url='/accounts/error')
def view_change_info(request):


    if request.method == 'POST':
        context = dict()
        user= request.user
        reguser= Registrovanikorisnik.objects.get(idkor=user)


        context["img"]= reguser.slika.url




    return render(request, 'change_profile_info.html', context)











@login_required( login_url='/accounts/error')
@user_passes_test(is_not_admin, login_url='/accounts/error')
def change_info(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST['stara-lozinka']
        new_password = request.POST['nova-lozinka']
        confirm_password = request.POST['potvrda-lozinke']
        img=""
        context={}
        if "fileUpload" in request.FILES:
            file = request.FILES["fileUpload"]
            reguser= Registrovanikorisnik.objects.get(idkor=user)
            if(reguser.slika!=file):
                reguser.slika= file
                reguser.save()
                messages.success(request, 'Slika je uspešno promenjena!')

        reguser = Registrovanikorisnik.objects.get(idkor=user)
        context["img"] = reguser.slika.url
        if old_password==""  and new_password=="" and confirm_password=="":
            return render(request, 'change_profile_info.html')

        if not check_password(old_password, user.password):
            messages.error(request, 'Stara lozinka nije ispravna!')


        elif new_password != confirm_password:
            messages.error(request, 'Lozinke se ne podudaraju. Molimo Vas unesite istu lozinku u oba polja!')

        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Lozinka je uspešno promenjena!')
        return render(request, 'change_profile_info.html', context)
    return render(request, 'change_profile_info.html')
