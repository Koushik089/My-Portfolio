from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "home.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # Validate required fields
        if not name or not email or not message:
            messages.error(request, 'All fields are required')
            return render(request, "components/contact.html")
        
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format')
            return render(request, "components/contact.html")

        full_message = f"""
        Name: {name}
        Email: {email}

        Message:
        {message}
        """

        try:
            send_mail(
                subject="New Contact Message from Portfolio",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
        except Exception as e:
            logger.exception("Failed to send contact email: %s", e)
            messages.error(request, 'Failed to send email. Please try again.')
            return render(request, "components/contact.html")

    return render(request, "components/contact.html")