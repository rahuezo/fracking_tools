from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
import csv
import os


def index(request):
    context = {
        'uploaded_urls': [1,2,3,4],
    }

    return render(request, 'pairwise_comparisons/index.html', context)


def example(request):
    return render(request, 'pairwise_comparisons/index.html')


def multi_file_upload(request):
    if request.method == 'POST' and request.FILES.getlist("comp-files"):
        comp_files = request.FILES.getlist("comp-files")

        fs = FileSystemStorage()

        uploaded_urls = []

        for f in comp_files:
            file_name = fs.save(f.name, f)
            uploaded_urls.append(fs.url(file_name))

        context = {
            'upload_status': True,
            'uploaded_urls': [url.split('/')[-1].replace('%20', ' ') for url in uploaded_urls],
        }

        return render(request, 'pairwise_comparisons/index.html', context)


def spreadsheet_upload(request):
    if request.method == 'POST' and request.FILES["comp-spreadsheet"]:
        spread_sheet = request.FILES["comp-spreadsheet"]

        fs = FileSystemStorage()

        file_name = fs.save(spread_sheet.name, spread_sheet)
        uploaded_url = fs.url(file_name)

        fs = FileSystemStorage()

        uploaded_urls = [f for f in os.listdir(fs.location) if not f.lower().endswith('.csv')]

        context = {
            'upload_status': True,
            'uploaded_urls': uploaded_urls,
            'upload_spreadsheet_status': True,
            'uploaded_spreadsheet_url': uploaded_url.split('/')[-1].replace('%20', ' '),
            'comparison_status': True,
        }

        return render(request, 'pairwise_comparisons/index.html', context)


def generate_comparison_summary(request):
    print "\n\n\n BEfore error"
    csv_file_name = request.POST.get('csv_file_name') + '.csv'
    print csv_file_name
    print "\n\n\n After error\n\n\n"
    csv_file_path = os.path.join(settings.MEDIA_ROOT, csv_file_name)

    with open(csv_file_path, 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        writer.writerow(['File A Path', 'File B Path'])

    return render(request, 'pairwise_comparisons/index.html')


def download_comparison_summary(request):
    # context = {
    #     'upload_status': True,
    #     'upload_spreadsheet_status': True,
    #
    # }
    # return render(request, 'pairwise_comparisons/index.html')

    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return render(request, 'pairwise_comparisons/index.html')
    raise Http40