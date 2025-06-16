def get_comparison(request):
    return request.session.get("comparison", [])


def add_to_comparison(request, product_id):
    comparison = get_comparison(request)
    if product_id not in comparison:
        comparison.append(product_id)
        request.session["comparison"] = comparison


def remove_from_comparison(request, product_id):
    comparison = get_comparison(request)
    if product_id in comparison:
        comparison.remove(product_id)
        request.session["comparison"] = comparison
