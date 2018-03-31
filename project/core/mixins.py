from collections import namedtuple

from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.settings import api_settings

from core.bl.utils_helper import prn


class SearchMixin:
    """
    Mixin for search data
    """
    queryset = None
    search_by_fields = []
    search_by_one_fields = []

    def get_queryset(self):
        queryset = self.search_by_field(self.queryset)
        queryset = self.search_by_one_field(queryset)
        return queryset

    def search_by_one_field(self, queryset):
        options = dict()
        for field in self.search_by_one_fields:
            value = self.request.query_params.get(field, None)
            if value is not None:
                options["%s__icontains" % field.replace('search_', '')] = value

        return queryset.filter(**options)

    def search_by_field(self, queryset):
        value = self.request.query_params.get('search', None)
        if value:
            value = value.strip()

        options = None
        for field in self.search_by_fields:
            if value is not None:
                q = Q(**{"%s__icontains" % field: value})

                if options:
                    options = options | q  # or & for filtering
                else:
                    options = q

        if options:
            queryset = queryset.filter(options)

        return queryset


class ExpandMixin:
    """
    Reusable mixin for expand function
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response = ProductServices.expands(request, instance, serializer.data, self.expandable)
        return Response(response)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            responses = ProductServices.expands_many(request, page, serializer.data, self.expandable)
            return self.get_paginated_response(responses)
        serializer = self.get_serializer(queryset, many=True)
        responses = ProductServices.expands_many(request, queryset, serializer.data, self.expandable)
        return Response(responses)


class ProductServices(object):
    """
    Service object. Used in order to store custom/read-expensive
    logic from core elemnts (views, models, serializers, etc.)
    """

    @staticmethod
    def serializer_update_extension(instance, materials_for_product):
        """
        Method deletes old material data from product in order to create new.
        :param instance: Object which data should be updated
        :param materials_for_product: 'list' of 'OrderedDict' wth:
                key-'material', val- Material instance
                key-'manufacture_quantity', val-'int'....
        :return: updates data
        """
        pass

    @staticmethod
    def order_objects(queryset, request):
        """
        Implements queryset ordering functionality
        :param queryset:
        :param request:
        :return: ordered queryset
        """
        if 'ordering' in request.query_params:
            queryset = queryset.order_by(request.query_params['ordering'])
        return queryset

    @staticmethod
    def filter_queryset(queryset, request):
        """
        Function uses for filtering ManufactureProduct 'stage' field for None value
        :param queryset:
        :param request:
        :return:
        """
        if request.query_params.get('nullable_stage') in ['True', 'False']:
            queryset = queryset.filter(stage__isnull=request.query_params.get('nullable_stage') == 'True')

        return queryset

    @staticmethod
    def expands(request, instance, response, expandable_fields, expand_args=None, expand_query=None):
        """
        Method implement EXPAND functionality
        :param request: Request Object
        :param instance: Model instance which fields will be expanded
        :param response: serialize.data
        :param expandable_fields: 'doc' characterizing specific fields and data from that fields to expand
            exapmle: {
            'draw': ['id', 'url'],
            'series': ['id', 'name'],
            'type': ['id', 'name'],
            'images': ['id', 'url']
        }
        :return: Response Object
        """
        if expand_args is None:
            expand_args = request.query_params.get('expand')

        if expand_args:

            for expand_arg in expand_args.split(','):
                new_field_name = expand_arg + '_exp'
                try:
                    expand_objects = getattr(instance, expand_arg)
                    # print(expand_objects, 'Expand_objects')
                except AttributeError:
                    response['ERROR'] = "Field '%s' can not be expanded or this field does not exist." % expand_arg
                    return response

                if expand_objects:

                    values_dict = {}
                    if hasattr(expand_objects, 'all'):
                        list_values = []
                        for obj in ProductServices.get_expand_query(expand_objects, expand_arg, expand_query):

                            for expandable_field in expandable_fields[expand_arg]:
                                ProductServices.set_values(obj, values_dict, expandable_field)
                            list_values.append(values_dict)
                            values_dict = {}

                        response[new_field_name] = list_values
                    else:

                        for expandable_field in expandable_fields[expand_arg]:
                            ProductServices.set_values(expand_objects, values_dict, expandable_field)
                        response[new_field_name] = values_dict

                elif not expand_objects:
                    response[new_field_name] = None

        return response

    @staticmethod
    def get_expand_query(expand_objects, expand_arg, expand_query):
        if expand_query and expand_arg in expand_query:
            return expand_query[expand_arg]
        else:
            return expand_objects.all()


    @staticmethod
    def set_values(obj, values_dict, expandable_field_source):

        if isinstance(expandable_field_source, dict):
            expandable_field = list(expandable_field_source.keys())[0]
            fields = expandable_field_source[expandable_field]

            obj_related = getattr(obj, expandable_field)

            values_dict[expandable_field] = {}
            if obj_related:
                for field in fields:
                    value_related = getattr(obj_related, field)
                    values_dict[expandable_field][field] = ProductServices.validate_value(value_related, field)
            else:
                values_dict[expandable_field] = None

        else:
            expandable_field = expandable_field_source
            value = getattr(obj, expandable_field)
            value = ProductServices.validate_value(value, expandable_field)
            values_dict[expandable_field] = value

        return values_dict

    @staticmethod
    def validate_value(value, expandable_field):
        if expandable_field != "id":
            return str(value)
        return value

    @staticmethod
    def expands_many(request, queryset, responses, expandable_fields, expand_args=None, expand_query=None):
        """
        The same as "expands" but work with queryset (many instances)
        """
        responses_list = []
        for instance, response in zip(queryset, responses):
            updated_resp = ProductServices.expands(request, instance, response, expandable_fields, expand_args, expand_query)
            if str(type(updated_resp)) == "<class 'rest_framework.response.Response'>":
                continue
            responses_list.append(updated_resp)
        return responses_list


ControlButton = namedtuple('ControlButton', 'label, link, icon, link_class, link_attrs')


class ControlsButton(object):
    list_display = []
    controls_button_list = []
    #controls_button_default = None
    can_delete = True
    options = {}

    def __init__(self, can_delete=True, options={}):
        #self.controls_button_default = None
        self.controls_button_list = []
        self.list_display = []
        self.can_delete = can_delete
        self.options = options

    def get_list_display(self, request):

        def controls_button(obj):
            self.set_controls_button_list(obj)
            context = dict()
            #context['controls_button_default'] = self.controls_button_default
            context['controls_button_list'] = self.controls_button_list
            return mark_safe(render_to_string('admin/components/controls_button.html', context))

        controls_button.short_description = 'Controls'
        controls_button.admin_order_field = ''
        self.list_display.append(controls_button)
        return self.list_display

    def set_controls_button_list(self, obj):
        """
        Override for change button position or add new buttons
        :return:
        """
        #self.controls_button_default = self.get_edit_button(obj)

        #self.controls_button_list.append(self.get_edit_button(obj, icon='icon-pencil'))
        can_edit = True
        if 'can_edit' in self.options:
            can_edit = self.options['can_edit']
        if can_edit:
            self.controls_button_list.insert(0, self.get_edit_button(obj, icon='icon-pencil'))

        # self.controls_button_list.append(self.get_history_button(obj))
        if self.can_delete:
            self.controls_button_list.append(self.get_delete_button(obj))

    def get_edit_button(self, obj, icon='icon-pencil icon-white'):
        label_name = 'Edit'
        if 'edit_button_name' in self.options:
            label_name = self.options['edit_button_name']

        return ControlButton(label=label_name,
                             link=self.get_link(obj=obj, link_type='change'),
                             icon=icon,
                             link_class='',
                             link_attrs='')

    def get_delete_button(self, obj):
        return ControlButton(label='',
                             link=self.get_link(obj=obj, link_type='delete'),
                             icon='icon-trash',
                             link_class='btn-danger caution-link',
                             link_attrs="data-caution-text='Are you sure you want to delete this entry?'")

    def get_history_button(self, obj):
        return ControlButton(label='History',
                             link=self.get_link(obj=obj, link_type='history'),
                             icon='icon-info-sign',
                             link_class='',
                             link_attrs='')

    # def get_divider(self):
    #     """
    #     Buttons separator
    #     :return:
    #     """
    #     return '<li class="divider"></li>'

    def get_link(self, obj, link_type='change'):
        """
        :param name:
        :param obj:
        :param link_type: edit, delete
        :return:
        """
        link_data = (obj._meta.app_label, obj._meta.object_name.lower(), link_type)
        link = reverse("admin:%s_%s_%s" % link_data, args=(obj.id, ))

        return link

    def get_list_controls(self, obj, set_default=True):
        if set_default:
            self.set_controls_button_list(obj)
        context = dict()
        #context['controls_button_default'] = self.controls_button_default
        context['controls_button_list'] = self.controls_button_list
        return mark_safe(render_to_string('admin/components/controls_button.html', context))
