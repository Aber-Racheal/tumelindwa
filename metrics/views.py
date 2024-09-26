from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import LocationSearch, Download
from django.db.models import Count, Q

@require_http_methods(["POST"])
def search_location(request):
    location = request.POST.get('location')
    
    flood_risk = get_flood_risk_for_location(location)
    search_record = LocationSearch.objects.create(
        location=location, 
        is_successful=flood_risk is not None
    )
    
    if flood_risk is None:
        return JsonResponse({'message': 'No flood risk data found'}, status=404)

    return JsonResponse({'location': location, 'flood_risk': flood_risk}, status=200)

@require_http_methods(["POST"])
def download_report(request):
    search_id = request.POST.get('search_id')
    try:
        search_record = LocationSearch.objects.get(id=search_id)
        Download.objects.create(location_search=search_record)
        return JsonResponse({'message': 'Report downloaded successfully'}, status=200)
    except LocationSearch.DoesNotExist:
        return JsonResponse({'message': 'Search record not found'}, status=404)

def get_flood_risk_for_location(location):
    flood_risk_data = {
        'Nairobi': 15,
        'Langata': 8,
        'Dandora': 30,
    }
    return flood_risk_data.get(location)

def statistics(request):
    total_searches = LocationSearch.objects.count()
    successful_searches = LocationSearch.objects.filter(is_successful=True).count()
    success_rate = (successful_searches / total_searches) * 100 if total_searches > 0 else 0
    
    total_downloads = Download.objects.count()

    return JsonResponse({
        'total_searches': total_searches,
        'successful_searches': successful_searches,
        'success_rate': success_rate,
        'total_downloads': total_downloads,
    })
