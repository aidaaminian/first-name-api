from django.http import JsonResponse
from mongoengine import DoesNotExist
from .models import FirstName
import json

def get_first_names(request):
    # Parse query parameters
    sort_order = request.GET.get('sort', 'asc')
    limit = request.GET.get('limit', None)
    
    # Build the query
    query = FirstName.objects
    
    # Apply sorting
    if sort_order == 'asc':
        query = query.order_by('name')
    elif sort_order == 'dec':
        query = query.order_by('-name')

    # Apply limit
    if limit is not None:
        try:
            limit = int(limit)
            query = query.limit(limit)
        except ValueError:
            return JsonResponse({'error': 'Invalid limit value'}, status=400)

    # Retrieve data
    names = [name.name for name in query]
    return JsonResponse(names, safe=False)

def search_by_name(request):
    # Parse query parameters
    sort_order = request.GET.get('sort', 'asc')
    limit = request.GET.get('limit', None)
    search_name = request.GET.get('substr', None)
    
    # Build the query
    query = FirstName.objects(name__icontains=search_name)
    
    # Apply sorting
    if sort_order == 'asc':
        query = query.order_by('name')
    elif sort_order == 'dec':
        query = query.order_by('-name')

    # Apply limit
    if limit is not None:
        try:
            limit = int(limit)
            query = query.limit(limit)
        except ValueError:
            return JsonResponse({'error': 'Invalid limit value'}, status=400)

    # Retrieve data
    names = [name.name for name in query]
    return JsonResponse(names, safe=False)

def add_first_name(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            
            # Create and save the new name
            new_name = FirstName(name=name)
            new_name.save()
            return JsonResponse({'message': 'Name added successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
