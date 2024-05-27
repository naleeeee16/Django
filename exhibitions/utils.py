from nft.views import get_nft_data
from .models import Listanft, Kolekcija, Pripada, Portfolio, Izlozba
from nft.models import Nft, Ocena


def create_context_for_nfts(nfts):
    nft_list = []
    for nft in nfts:
        nft_data = {
            'nft': nft,
            'data': None
        }
        if nft.slika == "":
            nft_data['data'] = get_nft_data(nft.url)

        nft_list.append(nft_data)

    context = {"nfts": nft_list}

    return context


def get_user_collection(user):
    lists_nft = Listanft.objects.filter(idvla=user)

    collection_user = None
    collections = Kolekcija.objects.all()
    for list_nft in lists_nft:
        for collection in collections:
            if list_nft == collection.idlis:
                collection_user = collection
                break

    return collection_user


def get_user_portfolio(user):
    lists_nft = Listanft.objects.filter(idvla=user)

    portfolio_user = None
    portfolios = Portfolio.objects.all()
    for list_nft in lists_nft:
        for portfolio in portfolios:
            if list_nft == portfolio.idlis:
                portfolio_user = portfolio
                break

    return portfolio_user


def get_nfts_from_collection(collection_user):
    nfts = []
    if collection_user:
        belong = Pripada.objects.filter(idlis=collection_user.idlis)
        nfts = [b.idnft for b in belong]

    return nfts


def get_nfts_from_exhibition(exhibition_user):
    return get_nfts_from_collection(exhibition_user)


def get_nfts_from_portfolio(portfolio_user):
    return get_nfts_from_collection(portfolio_user)


def get_list_attr(list_id):
    belong = Pripada.objects.filter(idlis=list_id)
    nfts = [b.idnft for b in belong]

    list_value = sum(nft.vrednost for nft in nfts)
    return list_value, len(nfts)


def set_list_attr(creator_list, list_value, list_len):
    list_nft = Listanft.objects.get(idlis=creator_list.idlis)
    list_nft.ukupnavrednost = list_value
    list_nft.brojnft = list_len
    list_nft.save()


def get_updated_exhibition_attr(request):
    selected_nfts = list(map(int, request.POST.get('selected_nfts').split(',')))
    nfts_objects = Nft.objects.filter(idnft__in=selected_nfts)

    exhibition_size = len(selected_nfts)

    exhibition_value = sum(nft.vrednost for nft in nfts_objects)

    grades = Ocena.objects.filter(idnft__in=nfts_objects)

    if grades.exists():
        exhibition_avg_grades = float(sum(grade.ocena for grade in grades)) / len(grades)
        print("\nBroj ocena kreiranje/izmenjene izlozbe je " + str(len(grades)))
    else:
        exhibition_avg_grades = 0
        print("\nBroj ocena kreiranje/izmenjene izlozbe je 0" + str(len(grades)))

    print("Ocene kreirane/izmenjene izlozbe su")
    for grade in grades:
        print("Ocena: " + str(grade.ocena))

    print("\n Prosek : " + str(exhibition_avg_grades))

    return nfts_objects, exhibition_size, exhibition_value, exhibition_avg_grades


def getRandomExhibitions():
    izlozba_ids = Izlozba.objects.values_list('idlis', flat=True)[:4]
    izlozbe = []
    for id in izlozba_ids:
        nft_list = []
        pripada_ids = Pripada.objects.filter(idlis=id).values_list('idnft', flat=True)
        izloz = Izlozba.objects.get(idlis=id)
        nfts = Nft.objects.filter(idnft__in=pripada_ids)

        cena = izloz.idlis.ukupnavrednost
        velicina = izloz.idlis.brojnft
        prosOc = izloz.prosecnaocena

        for nft in nfts:
            nft_data = {
                'nft': nft,
                'data': None
            }
            if nft.slika == "":
                nft_data['data'] = get_nft_data(nft.url)
            nft_list.append(nft_data)

        izlozba = {
            'id': izloz.idlis.idlis,
            'nfts': nft_list,
            'cena': cena,
            'naziv': izloz.naziv,
            'velicina': velicina,
            'prosecnaOcena': prosOc
        }
        izlozbe.append(izlozba)
    return izlozbe
