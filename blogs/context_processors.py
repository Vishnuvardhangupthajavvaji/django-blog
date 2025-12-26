from .models import Category, SocialMediaLink, About

def get_categories(request) :
    categories = Category.objects.all()
    return dict(categories=categories)


def get_social_links(request) :
    links = SocialMediaLink.objects.all()
    return dict(links=links)

def get_about(request) :
    about = About.objects.first()
    return dict(about=about)