# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import login, authenticate, logout
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .excel_handling import donemFileHandle, excelFileHandle, kelime_manipule
from .models import Dersler, BolumBaskani
import xlrd

def query_isim(isim, soy_isim):
    isim = kelime_manipule(kelime_manipule(isim, "İ", "i"),"I", "ı").lower()
    soy_isim= kelime_manipule(kelime_manipule(soy_isim, "İ", "i"), "I", "ı").lower()
    return f'{isim} {soy_isim}'

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('sistem:donem')
        return redirect('sistem:index')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username, password = password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('sistem:index')
    return render(request, 'login.html', {'form': form, 'title': 'Sisteme Giriş Yapın'})


def logout_view(request):
    logout(request)
    return redirect('sistem:login')


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.bolum = form.cleaned_data.get('Bolum')
            user.profile.fakulte = form.cleaned_data.get('Fakulte')
            user.save()
            #raw_password = form.cleaned_data.get('Sifre')
           # user = authenticate(username=user.username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('sistem:index')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form' : form,'title':'Sisteme Kayıt Olun'})


@login_required
def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['excelUpload']
            if file.name[-3:] != "xls" and file.name[-4:] != "xlsx":
                return render(request, 'upload.html', {'form': form, 'title': 'Lütfen Geçerli Bir Excel Dosyası Yükleyin'}) 
            excel = xlrd.open_workbook(file_contents=file.read())
            basTarih = form.cleaned_data.get('tarih1') 
            sonTarih = form.cleaned_data.get('tarih2')
            if basTarih >= sonTarih:
                return render(request, 'upload.html', {'form': form, 'title': 'Tarihleri Yanlış Girdiniz, Tekrar Girin'})
            dersler = Dersler.objects.filter(dersiVeren__exact=query_isim(request.user.first_name, request.user.last_name))
            if len(dersler) == 0:
                return render(request, 'upload.html', {'form': form, 'title': 'Adınıza Kayıtlı Ders Yok, Profilinizi Düzenleyin'})   
            return excelFileHandle(bas_tarih=basTarih, son_tarih=sonTarih, file=excel, dersler=dersler, request=request)
    form = UploadForm()
    return render(request, 'upload.html', {'form': form, 'title':'Excell Dosyasını Yükleyin'})


@staff_member_required
def donem_excel(request):
    if request.method == 'POST':
        form = AdminUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['excel']
            x = form.cleaned_data.get('bas_satir')
            y = form.cleaned_data.get('son_satir')
            excel = xlrd.open_workbook(file_contents=file.read())
            donemFileHandle(bas_satir=x-1, son_satir=y, file=excel)
            return render(request, 'donem.html', {'form':form, 'title': 'Dersler VeriTabanına Eklendi'})
    else:
        form = AdminUploadForm()
        return render(request, 'donem.html', {'form':form, 'title': 'Donemlik Excel Dosyasını Yükleyin'})


@login_required
def profile(request):
    dersler = Dersler.objects.filter(dersiVeren__exact=query_isim(request.user.first_name, request.user.last_name))
    try:
        bolum_baskani = BolumBaskani.objects.get(bolum=request.user.profile.bolum).ad
    except BolumBaskani.DoesNotExist:
        bolum_baskani = None
    if request.method == 'POST':
        u_form = UserUpdateForm (request.POST, instance= request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('sistem:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title' : 'Profilinizi Düzenleyin',
        'dersler': dersler,
        'bolum_baskani': bolum_baskani,
    }

    return render(request, 'profile.html', context)


@login_required
def dersler_view(request):
    dersler = Dersler.objects.filter(dersiVeren__exact=query_isim(request.user.first_name, request.user.last_name))
    if len(dersler) == 0:
        raise Http404('Sistemde Adınıza Kayıtlı Ders Bulunamadı, Adınızı Dogru Girdiginizden Emin Olun.')
    return render(request, 'dersler.html', {'dersler':dersler})

@login_required
def ders_update_view(request, id):
    dersler = Dersler.objects.filter(dersiVeren__exact=query_isim(request.user.first_name, request.user.last_name))
    ders = get_object_or_404(Dersler, id=id)
    form = DersForm(request.POST or None, instance = ders)
    if ders in dersler:
        if form.is_valid():
            ders = form.save()
            return redirect('sistem:dersler')
        return render(request, 'ders_update.html', {'form':form, 'ders':ders})
    raise Http404()


@login_required
def ders_create_view(request):
    dersler = Dersler.objects.filter(dersiVeren__exact=query_isim(request.user.first_name, request.user.last_name))
    if len(dersler) == 0:
        raise Http404('Sistemde Adınıza Kayıtlı Ders Olmadığı İçin Ders Yaratamazsınız, Adınızı Doğru Girdiğinizden Emin Olun.')
    form = DersForm(request.POST or None)
    ornek = dersler[0]
    if form.is_valid():
         ders = form.save(commit=False)
         ders.dersiVeren = ornek.dersiVeren
         ders.save()
         return redirect('sistem:dersler')
    return render(request, 'ders_create.html', {'form':form})


@login_required
def ders_delete_view(request, id):
    dersler = Dersler.objects.filter(dersiVeren__exact=query_isim(request.user.first_name, request.user.last_name))
    if len(dersler) > 1:
        ders = get_object_or_404(Dersler, id=id)
        if ders in dersler:
            ders.delete()
            return redirect('sistem:dersler')
        else:
            return Http404('Silemeye Çalıştığınız Ders Size Ait Değil !')
    return Http404('En Azından 1 Tane Dersiniz Sistemde Kalmalıdır.')
