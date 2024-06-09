from django.shortcuts import render
import requests 
from django.http import JsonResponse
import logging 
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

API_URL = "https://entire-elnore-sneakersdaily-b3c43214.koyeb.app/"

# Create your views here.
def index(request):
  return render(request=request , template_name='index.html' )

def connection_test(request):
    response = requests.get(API_URL)
    data = {"status": "success" if response.status_code == 200 else "failed"}
    return render(request=request , template_name='index.html' , context={'message' : data})

def predictView(request):
   return render(request=request , template_name='predict.html' )

def predict(request):
    if request.method == 'POST':
        try:
            # Mengambil data dari request POST
            ukuran = request.POST.get('ukuran_field')
            warna = request.POST.get('warna_field')
            harga = request.POST.get('harga_field')
            kategori = request.POST.get('kategori_field')
            bahan = request.POST.get('bahan_field')
            kondisi = request.POST.get('kondisi_field')

            # Check if any field is missing
            if not all([ukuran, warna, harga, kategori, bahan, kondisi]):
                missing_fields = [field for field, value in {
                    'ukuran_field': ukuran,
                    'warna_field': warna,
                    'harga_field': harga,
                    'kategori_field': kategori,
                    'bahan_field': bahan,
                    'kondisi_field': kondisi
                }.items() if not value]
                error_message = f"Missing fields: {', '.join(missing_fields)}"
                logger.error(error_message)
                return JsonResponse({'error': 'Invalid input', 'details': error_message}, status=400)

            # Mempersiapkan data untuk dikirim ke API
            payload = {
                'ukuran': ukuran,
                'warna': warna,
                'harga': harga,
                'kategori': kategori,
                'bahan': bahan,
                'kondisi': kondisi
            }

            # Log payload
            logger.info(f"Sending payload: {payload}")

            # Mengirim POST request ke API
            response = requests.post('https://entire-elnore-sneakersdaily-b3c43214.koyeb.app/predict', data=payload)

            # Log status code dan respons dari API
            logger.info(f"Received response: {response.status_code}, {response.text}")

            # Mengembalikan respons dari API
            if response.status_code == 200:
                return render(request=request , template_name='index.html' , context={'data' : response.json()})
            else:
                # Check if the response content type is HTML
                if 'text/html' in response.headers['Content-Type']:
                    # Parse HTML to extract error message
                    soup = BeautifulSoup(response.text, 'html.parser')
                    error_message = soup.get_text()
                    logger.error(f"Received HTML error response: {error_message}")
                    return JsonResponse({'error': 'Failed to get prediction', 'details': error_message}, status=response.status_code)
                else:
                    return JsonResponse({'error': 'Failed to get prediction', 'details': response.text}, status=response.status_code)
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return JsonResponse({'error': 'An error occurred during prediction', 'details': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)