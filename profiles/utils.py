from accounts.models import Korisnik
from nft.models import Nft
from profiles.models import Registrovanikorisnik


def create_main_context(request, username):

    user = Korisnik.objects.get(username=username)
    context = dict()
    context["id"] = user.idkor
    context["username"] = user.username
    context["image"] = Registrovanikorisnik.objects.get(idkor=user).slika.url
    context["type"] = user.user_type
    context["myprofile"] = False
    context["joined"]= Registrovanikorisnik.objects.get(idkor=user).datumkreiranja
    context["email"]=Registrovanikorisnik.objects.get(idkor=user).email
    context["buy_number"]=Registrovanikorisnik.objects.get(idkor=user).kupljenihNFT
    context["sell_number"]=Registrovanikorisnik.objects.get(idkor=user).prodatihNFT
    context["birthdate"]= Registrovanikorisnik.objects.get(idkor=user).datumrodjenja.strftime("%d/%m/%Y")
    context["num_of_nft"]=  Nft.objects.filter(idvla=user.idkor).count()

    if user.username == request.user.username:
        context["myprofile"] = True

    return context

