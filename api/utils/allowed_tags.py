def filter_endpoints_by_allowed_tags(result, generator, request, public):
    """
    Filtra endpoints que não possuem uma das tags permitidas.
    """
    allowed_tags = {
        'Usuário',
    }

    paths = result['paths']
    new_paths = {}

    for path, methods in paths.items():
        new_methods = {}
        for method, operation in methods.items():
            operation_tags = set(operation.get('tags', []))

            # Mantém apenas se tiver pelo menos uma tag permitida
            if operation_tags & allowed_tags:
                new_methods[method] = operation

        if new_methods:
            new_paths[path] = new_methods  # Adiciona os caminhos filtrados

    result['paths'] = new_paths
    return result