responses = {
    'project': {
        'get': {'project': {'name': 'Foo', 'id': 1, 'identifier': 'foo'}},
        'all': {'projects': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'issue': {
        'get': {'issue': {'subject': 'Foo', 'id': 1}},
        'all': {'issues': [{'subject': 'Foo', 'id': 1}, {'subject': 'Bar', 'id': 2}]},
        'filter': {'issues': [{'subject': 'Foo', 'id': 1}, {'subject': 'Bar', 'id': 2}]},
    },
    'time_entry': {
        'get': {'time_entry': {'hours': 2, 'id': 1}},
        'all': {'time_entries': [{'hours': 3, 'id': 1}, {'hours': 4, 'id': 2}]},
        'filter': {'time_entries': [{'hours': 3, 'id': 1}, {'hours': 4, 'id': 2}]},
    },
    'enumeration': {
        'filter': {'time_entry_activities': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'attachment': {
        'get': {'attachment': {'filename': 'foo.jpg', 'id': 1}},
    },
    'wiki_page': {
        'get': {'wiki_page': {'title': 'Foo', 'version': 1}},
        'filter': {'wiki_pages': [{'title': 'Foo', 'version': 1}, {'title': 'Bar', 'version': 2}]},
    },
    'project_membership': {
        'get': {'membership': {'id': 1}},
        'filter': {'memberships': [{'id': 1}, {'id': 2}]},
    },
    'issue_category': {
        'get': {'issue_category': {'id': 1, 'name': 'Foo'}},
        'filter': {'issue_categories': [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]},
    },
    'issue_relation': {
        'get': {'relation': {'id': 1}},
        'filter': {'relations': [{'id': 1}, {'id': 2}]},
    },
    'version': {
        'get': {'version': {'id': 1, 'name': 'Foo'}},
        'filter': {'versions': [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]},
    },
    'user': {
        'get': {'user': {'firstname': 'John', 'lastname': 'Smith', 'id': 1}},
        'all': {'users': [{'firstname': 'John', 'id': 1}, {'firstname': 'Jack', 'id': 2}]},
        'filter': {'users': [{'firstname': 'John', 'id': 1}, {'firstname': 'Jack', 'id': 2}]},
    },
    'group': {
        'get': {'group': {'name': 'Foo', 'id': 1}},
        'all': {'groups': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'role': {
        'get': {'role': {'name': 'Foo', 'id': 1}},
        'all': {'roles': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'news': {
        'all': {'news': [{'title': 'Foo', 'id': 1}, {'title': 'Bar', 'id': 2}]},
        'filter': {'news': [{'title': 'Foo', 'id': 1}, {'title': 'Bar', 'id': 2}]},
    },
    'issue_status': {
        'all': {'issue_statuses': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'tracker': {
        'all': {'trackers': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'query': {
        'all': {'queries': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'custom_field': {
        'all': {'custom_fields': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
}
