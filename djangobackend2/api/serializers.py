from rest_framework import serializers
from api.models import User

from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','tc','password','password2']
        extra_kwargs  = {'password':{'write_only':True}}
        
    # validating password and confirm password while registration
    def validate(self,attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if(password != password2):
            raise serializers.ValidationError('password and confirm password must match')
        return attrs
    
    def create(self,validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']
       
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']   
            
 # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs      
     
# class SendPasswordResetEmailSeriazlier(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)
#     class Meta:
#         fields = ['email']
        
#     def validate(self, attrs):
#         email = attrs.get('email')
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             print("Encoded UID", uid)
#             token = PasswordResetTokenGenerator().make_token(user)
#             link = "http://localhost:3000/api/user/reset/"+uid+"/"+token
#             print("password resset link", link)
            
#             # SEND EMAIL
#             body = 'Click following linkt to rest your password '+link
#             data = {
#                 'subject':'Password Reset',
#                 'body':body,
#                 'to_email':user.email
#             }
#             Util.send_email(data)
#             return attrs
#         else:
#             raise serializers.ValidationError("User with this email does not exists")
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')

        # Generate password reset token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct password reset URL
        reset_url = f"http://localhost:3000/reset-password/{uid}/{token}/"

        # Send email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return data
        
class UserPasswordResetSeriazlier(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']
        
    def validate(self, attrs):
        try:
            
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid') # encoded id
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid)) # decoded id
            user = User.objects.get(id = id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            return attrs 
        except DjangoUnicodeDecodeError as identifier:
            raise serializers.ValidationError("Token is not valid or expired")
         
    # def save(self, **kwargs):
    #     try:
    #         uid = force_bytes(urlsafe_base64_decode(kwargs.get('uid')))
    #         user = User.objects.get(id=uid)
    #         user.set_password(kwargs.get('password'))
    #         user.save()
    #         return user
    #     except Exception as e:
    #         raise serializers.ValidationError("The reset link is invalid", e)   