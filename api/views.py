import csv
import io
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Account, Lead, Email, MessageTemplate, SubjectTemplate
from .serializers import (
    AccountSerializer, LeadSerializer, EmailSerializer,
    MessageTemplateSerializer, SubjectTemplateSerializer
)
from .authentication import generate_token

User = get_user_model()


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email.lower())
        if password:
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        # If no password provided, allow login (simplified auth)
    except User.DoesNotExist:
        # Create user with default password if email-based auth is used
        default_password = password or 'default-password-123'
        user = User.objects.create_user(email=email.lower(), password=default_password)

    token = generate_token(user)

    response = Response({
        'message': 'Login successful',
        'token': token,
        'user': {'id': user.id, 'email': user.email}
    })

    # Set cookies
    response.set_cookie(
        'token',
        token,
        max_age=7 * 24 * 60 * 60,  # 7 days
        httponly=True,
        samesite='Lax',
        path='/'
    )
    response.set_cookie(
        'email',
        user.email,
        max_age=7 * 24 * 60 * 60,
        httponly=False,
        samesite='Lax',
        path='/'
    )

    return response


@api_view(['POST'])
def logout(request):
    response = Response({'message': 'Logout successful'})
    response.delete_cookie('token')
    response.delete_cookie('email')
    return response


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        if not serializer.validated_data.get('name'):
            raise serializers.ValidationError({'name': 'Account name is required'})
        serializer.save()


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(Email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(company__icontains=search)
            )
        
        # Status filter
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Assigned to filter
        assigned_to = self.request.query_params.get('assignedTo', None)
        if assigned_to:
            queryset = queryset.filter(assigned_to=assigned_to)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        # Handle both 'Email' and 'email' field names
        data = serializer.validated_data.copy()
        if 'email' in self.request.data and 'Email' not in data:
            data['Email'] = self.request.data['email']
        if not data.get('Email'):
            raise serializers.ValidationError({'Email': 'Email is required'})
        serializer.save(**data)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        
        # Read file content
        try:
            file_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response({'error': 'Invalid file encoding'}, status=status.HTTP_400_BAD_REQUEST)

        lines = [line.strip() for line in file_content.split('\n') if line.strip()]

        if len(lines) < 2:
            return Response({'error': 'CSV file must have at least a header and one data row'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Parse CSV
        def parse_csv_line(line):
            result = []
            current = ''
            in_quotes = False

            for char in line:
                if char == '"':
                    in_quotes = not in_quotes
                elif char == ',' and not in_quotes:
                    result.append(current.strip())
                    current = ''
                else:
                    current += char
            result.append(current.strip())
            return result

        # Parse header
        headers = [h.lower().replace(' ', '') for h in parse_csv_line(lines[0])]

        results = []
        errors = []
        processed = 0

        # Parse data rows
        for i, line in enumerate(lines[1:], start=2):
            values = parse_csv_line(line)
            row = {}

            for idx, header in enumerate(headers):
                if idx < len(values) and values[idx]:
                    row[header] = values[idx]

            if not row.get('email'):
                errors.append({'row': i, 'error': 'Email is required'})
                continue

            try:
                email = row['email'].lower().strip()
                
                # Check if lead already exists
                if Lead.objects.filter(Email=email).exists():
                    errors.append({'row': i, 'email': email, 'error': 'Lead already exists'})
                    continue

                lead_data = {
                    'Email': email,
                    'status': row.get('status', 'unused'),
                    'first_name': row.get('firstname') or row.get('first_name', ''),
                    'last_name': row.get('lastname') or row.get('last_name', ''),
                    'company': row.get('company', ''),
                    'title': row.get('title', ''),
                    'phone': row.get('phone', ''),
                    'linkedin': row.get('linkedin', ''),
                    'website': row.get('website', ''),
                    'city': row.get('city', ''),
                    'state': row.get('state', ''),
                    'country': row.get('country', ''),
                    'assigned_to': row.get('assignedto') or row.get('assigned_to') or None,
                }

                lead = Lead.objects.create(**lead_data)
                results.append(LeadSerializer(lead).data)
                processed += 1

            except Exception as e:
                errors.append({'row': i, 'error': str(e)})

        response_data = {
            'success': True,
            'processed': processed,
            'created': len(results),
        }

        if errors:
            response_data['errors'] = errors

        return Response(response_data, status=status.HTTP_200_OK)


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer

    def get_queryset(self):
        queryset = super().get_queryset().select_related('account')
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(email__icontains=search)
        
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        if not serializer.validated_data.get('email'):
            raise serializers.ValidationError({'email': 'Email is required'})
        
        email_data = serializer.validated_data.copy()
        email_data['email'] = email_data['email'].lower()
        
        account_id = self.request.data.get('accountId')
        if account_id:
            email_data['account_id'] = account_id
        
        serializer.save(**email_data)


class MessageTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(content__icontains=search) |
                Q(industry__icontains=search)
            )
        
        # Industry filter
        industry = self.request.query_params.get('industry', None)
        if industry:
            queryset = queryset.filter(industry__icontains=industry)
        
        return queryset.order_by('-created_at')


class SubjectTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubjectTemplate.objects.all()
    serializer_class = SubjectTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(content__icontains=search)
        
        return queryset.order_by('-created_at')

