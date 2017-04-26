from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
from . import getlatlon

def index(request):
    for file in os.listdir(settings.MEDIA_ROOT):
        os.remove(os.path.join(settings.MEDIA_ROOT, file))
    if request.method == 'POST' and request.FILES['images']:
        listoflatlong = []
        LIST = request.FILES.getlist('images')
        for file in LIST:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            imageurl = settings.BASE_DIR + uploaded_file_url
            print "imageurl : ", imageurl
            image = Image.open(imageurl)
            listoflatlong.append(getlatlon.get_lat_lon(image))
        return render(request, 'map/index.html', {'listoflatlong' : listoflatlong})
    return render(request, 'map/index.html')


