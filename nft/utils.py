from .models import *
from exhibitions.models import *


def first_time_grading(nft, reg_user):
    all_grades = Ocena.objects.filter(idkor=reg_user, idnft=nft)
    if all_grades:
        return False
    return True


def get_exhibitions_from_nft(nft):
    lists_where_nft_belongs = [b.idlis for b in Pripada.objects.filter(idnft=nft)]
    return [exhibition for exhibition in Izlozba.objects.all() if exhibition.idlis in lists_where_nft_belongs]


def update_exhibition_grade(exhibition, exhibition_nfts):
    grades = Ocena.objects.filter(idnft__in=exhibition_nfts)

    if grades.exists():
        exhibition.prosecnaocena = float(sum(grade.ocena for grade in grades)) / len(grades)
        print("\nBroj ocena apdejtovane izlozbe je " + str(len(grades)))
    else:
        exhibition.prosecnaocena = 0
        print("\nBroj ocena apdejtovane izlozbe je 0" + str(len(grades)))

    exhibition.save()

    print("Ocene apdejtovane izlozbe su")
    for grade in grades:
        print("Ocena: " + str(grade.ocena))

    print("\nBroj ocena apdejtovane izlozbe je" + str(len(grades)))
    print("\n Prosek : " + str(exhibition.prosecnaocena))



def get_nfts_from_exhibition(exhibition):
    nfts = []
    if exhibition:
        belong = Pripada.objects.filter(idlis=exhibition.idlis)
        nfts = [b.idnft for b in belong]

    return nfts


def update_nft_all_exhibitions_with_grades(nft):
    exhibitions = get_exhibitions_from_nft(nft)
    for exhibition in exhibitions:
        exhibition_nfts = get_nfts_from_exhibition(exhibition)
        update_exhibition_grade(exhibition, exhibition_nfts)

    return
