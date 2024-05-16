from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import *
import imagehub.settings as settings
from django.http import HttpResponseBadRequest

from .utils import TextToImageAPI

def index(request):
    return render(request, 'feed.html')
# def login_view(request):
#     return render(request='login_view')

def modelview(request):
    return render(request, 'input_form.html')
def payment_view(request):
    return render(request, 'payment.html') 

@login_required(login_url='login_view')
def generate_images(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt_1")
        model_choice = request.POST.get("model_choice")
        num_images = int(request.POST.get("num_images", 1))  # Default to 1 if not specified

        # Dictionary of API tokens for each model
        api_tokens = {
            "HuggingFace": "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",
            "animagine": "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",
            "stableDiffusion": "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",
            "AbsoluteReality": "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",
            "PlaygroundV2": "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",
        }

        try:
            # Use TextToImageAPI, not OpenAIapi
            text_to_image_api = TextToImageAPI(api_tokens)  
            image_bytes_list = text_to_image_api.generate_images(model_choice, prompt, num_images)

            # Process or return the images as needed
            image_bytes = image_bytes_list[0]
            image = Image.open(io.BytesIO(image_bytes))
            
            response = HttpResponse(content_type="image/jpeg")
            image.save(response, "JPEG")

            return response
        except ValueError as ve:
            return HttpResponseBadRequest(str(ve))
        except Exception as e:
            return HttpResponseBadRequest(f"Failed to generate image: {str(e)}")

    return render(request, "input_form.html")


def login_view(request):
    if request.user.is_authenticated:
        context = {
            'messages': 'You are already logged in'
        }
        return redirect('index')
    else:
        context = {
            'messages': 'Please login'
        }
    return render(request, 'login.html', context)

def signup_view(request):
    return render(request, 'signup.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            print("logged in")
            messages.success(request, 'Successfully logged in')
            return redirect('feed')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_view')

@login_required(login_url='login_view')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Successfully logged out')
    else:
        messages.warning(request, 'You are not logged in')

    return redirect('login_view')

def payment_view(request):
    return render(request, 'payment.html')  