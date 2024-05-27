
def is_admin(user):
    if user.user_type == 'admin':
        return True
    return False


def is_creator(user):
    if user.user_type == 'kreator':
        return True
    return False


def is_creator_or_collector(user):
    if user.user_type == 'kreator' or user.user_type == 'kolekcionar':
        return True
    return False


def is_not_admin(user):
    if user.user_type == 'admin':
        return False
    return True


def is_not_logged_in(user):
    if user.is_authenticated:
        return False
    return True


def is_logged_in(user):
    if user.is_authenticated:
        return True
    return False
