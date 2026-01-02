from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Member, Document, SignedDocument


def home(request):
    """Homepage"""
    return render(request, 'home.html')


def register(request):
    """Member registration"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        emergency_contact_name = request.POST.get('emergency_contact_name')
        emergency_contact_phone = request.POST.get('emergency_contact_phone')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            # Create member profile
            Member.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                emergency_contact_name=emergency_contact_name,
                emergency_contact_phone=emergency_contact_phone
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Double C Ranch.')
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register.html')


def user_login(request):
    """Login view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')


def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """Member dashboard"""
    # Check if user has member profile
    if not hasattr(request.user, 'member_profile'):
        if request.user.is_staff:
            return redirect('/admin/')
        messages.error(request, 'No member profile found. Please contact support.')
        return redirect('home')
    
    member = request.user.member_profile
    
    # Check for unsigned documents
    all_documents = Document.objects.filter(is_required=True)
    signed_doc_ids = member.signed_documents.values_list('document_id', flat=True)
    unsigned_documents = all_documents.exclude(id__in=signed_doc_ids)
    
    context = {
        'member': member,
        'unsigned_documents': unsigned_documents,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def sign_documents(request):
    """Sign required documents"""
    if not hasattr(request.user, 'member_profile'):
        messages.error(request, 'No member profile found.')
        return redirect('home')
    
    member = request.user.member_profile
    
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        document = Document.objects.get(id=document_id)
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Create signed document
        SignedDocument.objects.create(
            member=member,
            document=document,
            ip_address=ip
        )
        
        messages.success(request, f'Document "{document.title}" signed successfully.')
        return redirect('dashboard')
    
    # Get unsigned documents
    all_documents = Document.objects.filter(is_required=True)
    signed_doc_ids = member.signed_documents.values_list('document_id', flat=True)
    unsigned_documents = all_documents.exclude(id__in=signed_doc_ids)
    
    context = {
        'documents': unsigned_documents,
    }
    
    return render(request, 'sign_documents.html', context)
