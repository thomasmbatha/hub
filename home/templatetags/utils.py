# ==============================
# 📦 IMPORTS (Libraries you use)
# ==============================

import datetime
import json

from django.template import Context
from django.utils import translation
from django.apps import apps
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.urls import reverse, resolve, NoReverseMatch

from django.contrib.admin import AdminSite
from django.utils.text import capfirst, slugify
from django.contrib import messages, admin
from django.contrib.admin.options import IncorrectLookupParameters
from django.utils.translation import gettext_lazy as _
from collections import OrderedDict


# =====================================
# 🎨 DEFAULT ICONS FOR DJANGO APPS
# =====================================

default_apps_icon = {
    'auth': 'fa fa-users'
}


# =====================================
# 🌐 CUSTOM JSON RESPONSE (OPTIONAL)
# =====================================

class JsonResponse(HttpResponse):
    """
    Converts Python data into JSON response
    (Django already has this built-in, this is custom)
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('To allow non-dict objects, set safe=False')

        kwargs.setdefault('content_type', 'application/json')
        data = json.dumps(data, cls=encoder)

        super().__init__(content=data, **kwargs)


# =====================================
# 📋 GET ADMIN APP LIST (SIDEBAR MENU)
# =====================================

def get_app_list(context, order=True):
    """
    Builds the admin sidebar menu dynamically
    """
    admin_site = get_admin_site(context)
    request = context['request']

    app_dict = {}

    for model, model_admin in admin_site._registry.items():

        app_icon = getattr(model._meta.app_config, 'icon', None)
        app_label = model._meta.app_label

        # Check permissions
        has_module_perms = model_admin.has_module_permission(request)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            if True in perms.values():
                info = (app_label, model._meta.model_name)

                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                    'model_name': model._meta.model_name
                }

                # 🔗 Admin URLs
                if perms.get('change') or perms.get("view"):
                    try:
                        model_dict['admin_url'] = reverse(
                            f'admin:{info[0]}_{info[1]}_changelist',
                            current_app=admin_site.name
                        )
                    except NoReverseMatch:
                        pass

                if perms.get('add'):
                    try:
                        model_dict['add_url'] = reverse(
                            f'admin:{info[0]}_{info[1]}_add',
                            current_app=admin_site.name
                        )
                    except NoReverseMatch:
                        pass

                # Add app if not exists
                if app_label not in app_dict:
                    app_dict[app_label] = {
                        'name': apps.get_app_config(app_label).verbose_name,
                        'app_label': app_label,
                        'app_url': reverse(
                            'admin:app_list',
                            kwargs={'app_label': app_label},
                            current_app=admin_site.name,
                        ),
                        'has_module_perms': has_module_perms,
                        'models': [],
                    }

                app_dict[app_label]['models'].append(model_dict)

                # Assign icon
                if not app_icon:
                    app_icon = default_apps_icon.get(app_label)

                app_dict[app_label]['icon'] = app_icon

    app_list = list(app_dict.values())

    # Sort apps + models
    if order:
        app_list.sort(key=lambda x: x['name'].lower())

        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

    return app_list


# =====================================
# 🧭 GET CURRENT ADMIN SITE
# =====================================

def get_admin_site(context):
    """
    Detects which admin site is being used
    """
    try:
        request = context.get('request')
        current_resolver = resolve(request.path)
        namespace = current_resolver.namespaces[0]

        index_resolver = resolve(reverse(f'{namespace}:index'))

        if hasattr(index_resolver.func, 'admin_site'):
            return index_resolver.func.admin_site

        for closure in index_resolver.func.__closure__ or []:
            if isinstance(closure.cell_contents, AdminSite):
                return closure.cell_contents

    except Exception:
        pass

    return admin.site


# =====================================
# 🏷️ ADMIN SITE NAME
# =====================================

def get_admin_site_name(context):
    return get_admin_site(context).name


# =====================================
# ✅ SUCCESS MESSAGE MIXIN (FOR FORMS)
# =====================================

class SuccessMessageMixin:
    """
    Shows success message after form submit
    """

    success_message = ''

    def form_valid(self, form):
        response = super().form_valid(form)

        success_message = self.get_success_message(form.cleaned_data)

        if success_message:
            messages.success(self.request, success_message)

        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data


# =====================================
# 📊 GET MODEL DATA (ADMIN TABLE)
# =====================================

def get_model_queryset(admin_site, model, request, preserved_filters=None):
    """
    Gets queryset for admin table view
    """

    model_admin = admin_site._registry.get(model)

    if not model_admin:
        return

    try:
        reverse(
            f'{admin_site.name}:{model._meta.app_label}_{model._meta.model_name}_changelist'
        )
    except NoReverseMatch:
        return

    queryset = model_admin.get_queryset(request)

    return queryset


# =====================================
# 🌍 LANGUAGE HELPERS
# =====================================

def get_possible_language_codes():
    language_code = translation.get_language()
    language_code = language_code.replace('_', '-').lower()

    codes = [language_code]

    parts = language_code.split('-', 1)

    if len(parts) == 2:
        codes.append(parts[0])

    return codes


# =====================================
# 🔐 AUTH CHECK (MODERN DJANGO)
# =====================================

def user_is_authenticated(user):
    return user.is_authenticated


# =====================================
# 🔄 CONTEXT → DICTIONARY
# =====================================

def context_to_dict(context):
    """
    Converts Django template context to dictionary
    """
    if isinstance(context, Context):
        flat = {}
        for d in context.dicts:
            flat.update(d)
        return flat

    return context

def get_menu_items(context):
    """
    Dummy function to prevent ImportError.
    Replace this with real menu logic later.
    """
    return []