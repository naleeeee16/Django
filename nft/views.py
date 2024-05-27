from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect

import requests

from common.decoraters import is_creator


from .utils import *

from urllib.parse import urlparse

# Obavezno se dodaje u Header Request-a
API_KEY = "e0d9ad00e95945918aec9ec56c057650"


# Ova funkcija ce mozda trebati da bi se od url koji se cuva u bazi mogla dobiti slika i podaci
# Pozove se ova funkcija sa zadatim url-om i koristi se na sledeci nacin:
# nft = Nft.object.get(idnft = ...)
# nft_url = nft.url
# data = get_nft_data(nft_url)
# data.nft.image_url -> url koji se stavlja u src atribut za slike u .html fajlovima

def get_nft_data(nft_url):
    parsed_url = urlparse(nft_url)
    path_parts = parsed_url.path.split('/')
    chain = path_parts[-3]
    nft_contract_address = path_parts[-2]
    nft_token_id = path_parts[-1]

    api_url = 'https://api.opensea.io/api/v2/chain/' + chain + '/contract/' + nft_contract_address + '/nfts/' + nft_token_id
    headers = {
        "Accept": "application/json",
        "X-API-KEY": "e0d9ad00e95945918aec9ec56c057650"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def check_nft_param(file, name, price, description, creator, owner):
    # TODO
    return True


@login_required(login_url='/accounts/error')
@user_passes_test(is_creator, login_url='/accounts/error')
def create_nft(request):
    if request.method == 'POST':
        if "fileUpload" in request.FILES:
            file = request.FILES["fileUpload"]
        else:
            file = None

        if "nft_url" in request.POST:
            nft_url = request.POST["nft_url"]
        else:
            nft_url = None

        name = request.POST["nftName"]
        price = float(request.POST["nftPrice"])
        description = request.POST["nftDescription"]

        creator = Registrovanikorisnik.objects.get(idkor=request.user)
        owner = creator

        # Provera da li su dobro uneti parametri
        if check_nft_param(file, name, price, description, creator, owner):

            # Napravi objekat nft sa datim parametrima i sacuva ga u bazi
            if file is not None:
                nft = Nft(naziv=name, vrednost=price, opis=description, slika=file, idkre=creator, idvla=owner, url="")
            else:
                nft = Nft(naziv=name, vrednost=price, opis=description, slika="", idkre=creator, idvla=owner,
                          url=nft_url)

            nft.save()

            creator_lists = Listanft.objects.filter(idvla=creator)
            all_collections = Kolekcija.objects.all()
            for creator_list in creator_lists:
                for collection in all_collections:
                    if creator_list == collection.idlis:

                        belong = Pripada(idlis=creator_list, idnft=nft)
                        belong.save()

                        creator_list.ukupnavrednost += nft.vrednost
                        creator_list.brojnft += 1
                        creator_list.save()

            if request.user.user_type == 'kreator':
                all_portfolios = Portfolio.objects.all()
                for creator_list in creator_lists:
                    for portfolio in all_portfolios:
                        if creator_list == portfolio.idlis:

                            belong = Pripada(idlis=creator_list, idnft=nft)
                            belong.save()

                            creator_list.ukupnavrednost += nft.vrednost
                            creator_list.brojnft += 1
                            creator_list.save()

            return redirect('index')

        else:
            #TODO
            print("Error")

    return render(request, 'create_nft.html')


def nft_review(request, idnft):
    nft = Nft.objects.get(idnft=idnft)
    nft_data = {
        'nft': nft,
        'data': None
    }
    if nft.slika == "":
        nft_data['data'] = get_nft_data(nft.url)

    context = {"nft": nft_data}
    context["owner"] = nft.idvla.idkor
    context["creator"] = nft.idkre.idkor

    return render(request, 'nft_review.html', context)


from django.db.models import Avg


@login_required(login_url='/accounts/error')
def grade_nft(request):
    if request.method == 'POST':
        if 'rating' in request.POST:
            rating = int(request.POST['rating'])
        else:
            rating = None
        idnft = int(request.POST['idnft_name'])
        nft = Nft.objects.get(idnft=idnft)
        ocenio = Registrovanikorisnik.objects.get(idkor=request.user)

        context = dict()

        nft_data = {
            'nft': nft,
            'data': None
        }
        if nft.slika == "":
            nft_data['data'] = get_nft_data(nft.url)

        context = {"nft": nft_data}
        context["owner"] = nft.idvla.idkor
        context["creator"] = nft.idkre.idkor


        #provera rejtinga
        if first_time_grading(idnft, ocenio):

            if rating is not None and 0 < rating < 6:

                ocena = Ocena(ocena=rating, idnft=nft, idkor=ocenio)

                ocena.save()

                prosecna_ocena = Ocena.objects.filter(idnft=nft).aggregate(avg_rating=Avg('ocena'))['avg_rating']

                nft.prosecnaocena = prosecna_ocena
                nft.save()

                update_nft_all_exhibitions_with_grades(nft)

                messages.success(request, "Uspešno ste ocenili NFT!")
                return render(request, 'nft_review.html', context)

            else:
                messages.error(request, "Morate izabrati ocenu!")
                return render(request, 'nft_review.html', context)

        else:
            # Logika kako da obavestim korisnika da je vec ocenio
            messages.error(request, "Vec ste ocenili ovaj NFT!")
            return render(request, 'nft_review.html', context)


    else:
        return HttpResponseNotAllowed(['POST'])

    #return render(request, 'nft_review.html', {'idnft': request.GET.get('idnft')})


@login_required(login_url='/accounts/error')
def change_price(request):
    if request.method == 'POST':
        nova_cena = int(request.POST['new_price'])
        idnft = int(request.POST['idnft_name'])
        nft = Nft.objects.get(idnft=idnft)

        nft_data = {
            'nft': nft,
            'data': None
        }
        if nft.slika == "":
            nft_data['data'] = get_nft_data(nft.url)

        context = {"nft": nft_data}
        context["owner"] = nft.idvla.idkor
        context["creator"] = nft.idkre.idkor

        if nova_cena is not None and nova_cena != '':
            stara_cena = nft.vrednost
            nft.vrednost = nova_cena
            nft.save()

            nft_se_nalazi = Pripada.objects.filter(idnft=nft)
            liste = [l.idlis for l in nft_se_nalazi]
            for l in liste:
                l.ukupnavrednost += nova_cena - stara_cena
                l.save()

        return render(request, 'nft_review.html', context)

    else:
        return HttpResponseNotAllowed(['POST'])

    #return render(request, 'nft_review.html', {'idnft': request.GET.get('idnft')})


def buy_nft(request):
    if request.method == 'POST':
        idnft = int(request.POST['idnft_name'])
        nft = Nft.objects.get(idnft=idnft)

        platio = Registrovanikorisnik.objects.get(idkor=request.user)

        platio.kupljenihNFT += 1

        platio.save()

        prosli_vlasnik = nft.idvla

        prosli_vlasnik.prodatihNFT += 1

        prosli_vlasnik.save()
        nft.idvla = platio

        nft.save()

        prosli_vlasnik_kolekcije = Listanft.objects.filter(idvla=prosli_vlasnik)

        for kol in prosli_vlasnik_kolekcije:
            if not Portfolio.objects.filter(idlis=kol).exists():
                if Izlozba.objects.filter(idlis=kol).exists() and Pripada.objects.filter(idlis=kol, idnft = nft).exists():
                    Pripada.objects.filter(idlis=kol, idnft=nft).delete()
                    izlozba = Izlozba.objects.get(idlis=kol)
                    nft_izlozbe = get_nfts_from_exhibition(izlozba)
                    update_exhibition_grade(izlozba, nft_izlozbe)
                else:
                    Pripada.objects.filter(idlis=kol, idnft=nft).delete()

                kol.ukupnavrednost -= nft.vrednost
                kol.brojnft -= 1
                kol.save()


        platio_kolekcija = Listanft.objects.filter(idvla=platio)
        for kol in platio_kolekcija:
            if Kolekcija.objects.filter(idlis=kol).exists():
                Pripada.objects.create(idlis=kol, idnft=nft)
                kol.ukupnavrednost += nft.vrednost
                kol.brojnft += 1
                kol.save()


        # Treba da se doda da se u svakoj izlozbi promeni atributi
        nft_data = {
            'nft': nft,
            'data': None
        }
        if nft.slika == "":
            nft_data['data'] = get_nft_data(nft.url)

        context = {"nft": nft_data}
        context["owner"] = nft.idvla.idkor
        context["creator"] = nft.idkre.idkor

        return render(request, 'nft_review.html', context)

    else:
        return HttpResponseNotAllowed(['POST'])

    #return render(request, 'nft_review.html', {'idnft': request.GET.get('idnft')})
