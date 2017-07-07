# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from netcomp_utils.build_matrix import AdjacencyMatrix

from django.shortcuts import render
from .forms import CsvForm
from .models import CsvDocument
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import os, shutil
from django.conf import settings
from zipfile import ZipFile
import StringIO


def remove_netcomp_media():
    media_root = settings.MEDIA_ROOT
    
    print "Removing media and records from database...\n"
    
    all_csv_docs = CsvDocument.objects.all()
    
    for csv_doc in all_csv_docs:
        csv_doc.delete()
    
    shutil.rmtree(media_root, ignore_errors=True)
    
def index(request):
    remove_netcomp_media()
    
    context = {}
    
    return render(request, 'netcomp/index.html', context)


def build_networks_from_events(request):
    # Handle file upload
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist('csv_file')
            output_zip_name = request.POST.get('output_zip_name').upper().replace(' ', '_')
            
            for f in files:
                new_doc = CsvDocument(root_dir=output_zip_name, csv_file=f)

                new_doc.save()

            fs = FileSystemStorage()
            
            relationships_path = os.path.join(fs.location, output_zip_name)
            relationships_files = [f for f in os.listdir(relationships_path) if 'events' in f.lower()]
            
            files_to_zip = []
            
            for f in relationships_files:
                # Create adjacency matrix
                fpath = os.path.join(relationships_path, f)
                
                admat = AdjacencyMatrix(fpath, output_dir=relationships_path)
                matfile = admat.run()
                
                files_to_zip.append(matfile)
            
            print files_to_zip    
            
            with ZipFile("{0}.zip".format(os.path.join(relationships_path, output_zip_name)), 'w') as zf:
                for fpath in files_to_zip:    
                    zf.write(fpath, os.path.basename(fpath))
                    
            

            messages.success(request, "{0}.zip".format("{0}/{1}".format(output_zip_name, output_zip_name)))

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('netcomp:file_upload'))

    else:
        form = CsvForm()  # An empty form

    # Render list page with the documents and the form
    context = {
        'form': form,
    }
    
    return render(request, 'netcomp/events_network.html', context)


def build_networks_from_pairs(request):    
    # Handle file upload
    if request.method == 'POST':
        form = CsvForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist('csv_file')
            output_zip_name = request.POST.get('output_zip_name').upper().replace(' ', '_')
            
            for f in files:
                new_doc = CsvDocument(root_dir=output_zip_name, csv_file=f)

                new_doc.save()

            fs = FileSystemStorage()
            
            relationships_path = os.path.join(fs.location, output_zip_name)
            relationships_files = [f for f in os.listdir(relationships_path) if 'node_pairs' in f.lower()]
            
            files_to_zip = []
            
            for f in relationships_files:
                # Create adjacency matrix
                fpath = os.path.join(relationships_path, f)
                
                admat = AdjacencyMatrix(fpath, output_dir=relationships_path, csv_type='pairs')
                matfile = admat.run_pairs()
                
                files_to_zip.append(matfile)
            
            print files_to_zip    
            
            with ZipFile("{0}.zip".format(os.path.join(relationships_path, output_zip_name)), 'w') as zf:
                for fpath in files_to_zip:    
                    zf.write(fpath, os.path.basename(fpath))
                    
            

            messages.success(request, "{0}.zip".format("{0}/{1}".format(output_zip_name, output_zip_name)))

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('netcomp:file_upload_pairs'))

    else:
        form = CsvForm()  # An empty form

    # Render list page with the documents and the form
    context = {
        'form': form,
    }
        
    return render(request, 'netcomp/pairs_network.html', context)


def download_events_zip(request):
    zip_file_to_download = request.POST.get('zip-file-download')
    zip_file_to_download_path = settings.MEDIA_ROOT + '/' + zip_file_to_download
    
    with open(zip_file_to_download_path, 'rb') as zf:
        zf_content = zf.read()
    
    response = HttpResponse(zf_content, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(zip_file_to_download.split('/')[-1])
    
    return response
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    