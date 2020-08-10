from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from shop.models import Clothing, Payment

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):

    #email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)
    clothings = serializers.HyperlinkedRelatedField(
        view_name='clothing-detail', 
        read_only=True,
        many=True)
    payments = serializers.HyperlinkedRelatedField(
        view_name='pay',
        read_only=True,
        many=True
    )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        #user.set_password(validated_data['password'])
        #user.save()
        return user

    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','password','clothings']
        read_only_fields = ['id',]

class ClothingSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.email')
    payments = serializers.HyperlinkedRelatedField(
        view_name='pay',
        read_only=True,
        many=True
    )

    class Meta:
        model = Clothing
        fields = ['url','id','user','slug','name','date_created','price','category','number']

class PaymentSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.email')
    clothing = serializers.ReadOnlyField(source='clothing.id')
    class Meta:
        model = Payment
        fields = ['url','id','user','clothing','date_created']

