from .models import NavItem


def ventures_nav(request):
    items = list(NavItem.objects.filter(is_active=True).order_by('order'))
    if not items:
        items = [
            NavItem(label='Home', url_name='ventures:home', order=1),
            NavItem(label='About', url_name='ventures:about', order=2),
        ]

    current_url_name = ''
    if getattr(request, 'resolver_match', None):
        current_url_name = request.resolver_match.url_name or ''

    return {
        'ventures_nav_items': items,
        'ventures_current_url_name': current_url_name,
    }
