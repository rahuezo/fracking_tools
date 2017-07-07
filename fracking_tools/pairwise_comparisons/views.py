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
            
            output_csv_file_name = request.POST.get('csv_file_name')
            
            current_session_storage = ' '.join(output_csv_file_name.split()).upper().replace(' ', '_')
            
            for f in files:
                new_doc = Document(root_dir=current_session_storage, doc_file=f)

                new_doc.save()

            new_csv = Document(root_dir=current_session_storage, doc_file=csv_file)
            new_csv.save()

            comparison_summary = generate_comparison_summary(current_session_storage, output_csv_file_name, csv_file)

            messages.success(request, comparison_summary)

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('pairwise_comparisons:file_upload'))

    else:
        form = DocumentForm()  # An empty form

    # Render list page with the documents and the form
    context = {
        'form': form,
    }
    return render(request, 'pairwise_comparisons/index.html', context)


def generate_comparison_summary(home_dir, output_csv_file_name, pairs_file):
    working_directory = os.path.join(settings.MEDIA_ROOT, home_dir)
    
    csv_file_path = os.path.join(working_directory, output_csv_file_name) + '.csv'

    with open(csv_file_path, 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')

        writer.writerow(['File A', 'File B', 'Cosine Similarity', 'Jaccard Similarity'])

        # Get files to compare

        files = get_files_to_compare(pairs_file)

        rows = compare_files(working_directory, files)

        for row in rows:
            writer.writerow(row)

    uploaded_csv_url = "{0}/{1}".format(home_dir, [f for f in os.listdir(working_directory) if output_csv_file_name in f][0])

    return uploaded_csv_url


def download_comparison_summary(request):

    csv_file_to_download = request.POST.get('csv-file-download')
    csv_file_to_download_path = settings.MEDIA_ROOT + '/' + csv_file_to_download

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(csv_file_to_download.split('/')[-1])

    with open(csv_file_to_download_path, 'rb') as csv_file:
        response = HttpResponse(csv_file.read())
        response['content_type'] = 'text/csv'
        response['Content-Disposition'] = 'attachment;filename={0}'.format(csv_file_to_download.split('/')[-1])

        return response

