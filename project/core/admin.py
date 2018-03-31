

class MetaMixinAdmin(object):
    list_display_seo = ['seo_title', 'seo_description']

    fieldsets = (
        ('Seo tags',
            {'fields': ('seo_title', 'seo_description', )}),
    )
