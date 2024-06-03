import csv

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import CSVUploadForm, UserRegistrationForm, AssignForm, UserCreationForm, UserAssociationForm
from .models import Tool


@login_required
def tool_list(request):
    query = request.GET.get('q', '')
    if query:
        tools = Tool.objects.filter(
            Q(name__icontains=query) |
            Q(tool_type__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        tools = Tool.objects.all()
    return render(request, 'toolshed/tool_list.html', {'tools': tools, 'query': query})



@login_required
def assign_tool(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    if request.method == 'POST':
        form = AssignForm(request.POST)
        if form.is_valid():
            tool.assigned_to = form.cleaned_data['user']
            tool.is_checked_out = False
            tool.checked_out_by = None
            tool.save()
            return redirect('tool_list')
    else:
        form = AssignForm()
    return render(request, 'toolshed/assign_tool.html', {'form': form, 'tool': tool})


@login_required
def checkout_tool(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    if request.method == 'POST':
        tool.is_checked_out = True
        tool.checked_out_by = request.user
        tool.save()
        return redirect('tool_list')
    return render(request, 'toolshed/checkout_tool.html', {'tool': tool})


@login_required
def checkin_tool(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    if request.method == 'POST':
        tool.is_checked_out = False
        tool.checked_out_by = None
        tool.save()
        return redirect('tool_list')
    return render(request, 'toolshed/checkin_tool.html', {'tool': tool})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('tool_list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'toolshed/register.html', {'form': form})



@login_required
def import_tools(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            new_users = set()
            tools_data = []

            for row in reader:
                custodian_usernames = row['Custodian'].split(', ')
                custodians = []
                for username in custodian_usernames:
                    custodian = User.objects.filter(username=username.strip()).first()
                    if not custodian:
                        new_users.add(username.strip())
                    custodians.append(username.strip())

                tools_data.append({
                    'name': row['Tool'],
                    'type': row['Type'],
                    'battery': row['Battery'] if row['Battery'] != 'NaN' else None,
                    'custodians': custodians,
                    'location': row['Location'],
                    'is_checked_out': row['Checkout'].lower() == 'true'
                })

            # Store tools_data in session to process after user association/creation
            request.session['tools_data'] = tools_data
            request.session['new_users'] = list(new_users)

            if new_users:
                messages.info(request, 'Some users need to be associated or created.')
                return redirect('associate_users')

            return process_tools_import(request)
    else:
        form = CSVUploadForm()
    return render(request, 'toolshed/import_tools.html', {'form': form})

@login_required
def associate_users(request):
    new_users = request.session.get('new_users', [])
    if request.method == 'POST':
        form = UserAssociationForm(request.POST, new_users=new_users)
        if form.is_valid():
            user_associations = {}
            for new_user in new_users:
                associated_user_id = form.cleaned_data[f'user_{new_user}']
                if associated_user_id == 'create_new':
                    # Create new user
                    user = User.objects.create(username=new_user)
                    messages.success(request, f'User {user.username} created successfully.')
                    user_associations[new_user] = user.id
                else:
                    # Associate with existing user
                    user = User.objects.get(id=associated_user_id)
                    user_associations[new_user] = user.id
            request.session['user_associations'] = user_associations
            return process_tools_import(request)
    else:
        form = UserAssociationForm(new_users=new_users)
    return render(request, 'toolshed/associate_users.html', {'form': form, 'new_users': new_users})

@login_required
def process_tools_import(request):
    tools_data = request.session.get('tools_data', [])
    user_associations = request.session.get('user_associations', {})

    for tool_data in tools_data:
        custodians = [User.objects.get(id=user_associations.get(username, None)) for username in tool_data['custodians']]
        main_custodian = custodians[0] if custodians else None

        Tool.objects.update_or_create(
            name=tool_data['name'],
            defaults={
                'tool_type': tool_data['type'],
                'battery': tool_data['battery'],
                'custodian': main_custodian,
                'location': tool_data['location'],
                'is_checked_out': tool_data['is_checked_out']
            }
        )

    messages.success(request, 'Tools imported successfully.')
    return redirect('tool_list')

@login_required
def create_users(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully.')
            return redirect('import_tools')
    else:
        form = UserCreationForm()
    return render(request, 'toolshed/create_users.html', {'form': form})
