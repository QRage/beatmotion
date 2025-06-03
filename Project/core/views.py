from django.shortcuts import render

from pathlib import Path


def home_view(request):
    BASE_DIR = Path(__file__).resolve().parent.parent  # ← = Project
    base_path = BASE_DIR / 'templates' / 'base.html'
    return render(request, 'core/home.html')