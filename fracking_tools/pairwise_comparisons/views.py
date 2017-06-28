from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect

from django.conf import settings
import csv
import os

from django.core.urlresolvers import reverse
from .models import Document
from .forms import DocumentForm
from django.contrib import messages

from utils.get_files_to_compare import get_files_to_compare
from utils.compare_files import compare_files


def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist('doc_file')
            csv_file = request.FILES['csv_file']

            for f in files:
                new_doc = Document(doc_file=f)

                new_doc.save()

            new_csv = Document(doc_file=csv_file)
            new_csv.save()

            output_csv_file_name = request.POST.get('csv_file_name')

            comparison_summary = generate_comparison_summary(output_csv_file_name, csv_file)

            messages.success(request, comparison_summary)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('pairwise_comparisons:file_upload'))

    else:
        form = DocumentForm()  # An empty form

    # Load documents for the list page

    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {
        'documents': documents,
        'form': form,
    }
    return render(request, 'pairwise_comparisons/index.html', context)


def generate_comparison_summary(output_csv_file_name, pairs_file):
    csv_file_path = os.path.join(settings.MEDIA_ROOT, output_csv_file_name) + '.csv'

    with open(csv_file_path, 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        writer.writerow(['File A', 'File B', 'Cosine Similarity'])

        # Get files to compare

        files = get_files_to_compare(pairs_file)

        rows = compare_files(settings.MEDIA_ROOT, files)

        for row in rows:
            writer.writerow(row)

    fs = FileSystemStorage()

    uploaded_csv_url = [f for f in os.listdir(fs.location) if output_csv_file_name in f][0]

    return uploaded_csv_url


def download_comparison_summary(request):

    csv_file_to_download = request.POST.get('csv-file-download')
    csv_file_to_download_path = settings.MEDIA_ROOT + '/' + csv_file_to_download

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(csv_file_to_download)

    with open(csv_file_to_download_path, 'rb') as csv_file:
        response = HttpResponse(csv_file.read())
        response['content_type'] = 'text/csv'
        response['Content-Disposition'] = 'attachment;filename={0}'.format(csv_file_to_download)

        return response

