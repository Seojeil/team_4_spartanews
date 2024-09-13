from rest_framework import serializers
from .models import User


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'nickname', 'birth', 'gender', 'bio',)

    def validate(self, attrs):
        instance = self.instance
        if User.objects.filter(email=attrs['email']).exclude(id=instance.id).exists():
            raise serializers.ValidationError({"email": "이미 사용중인 이메일입니다."})
        return attrs

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.nickname = validated_data["nickname"]
        instance.birth = validated_data["birth"]
        instance.gender = validated_data["gender"]
        instance.bio = validated_data["bio"]

        instance.save()
        return instance


class UserChangePasswordSerailizers(serializers.Serializer):
    prev_password = serializers.CharField(write_only=True, required=True)
    password_1 = serializers.CharField(write_only=True, required=True)
    password_2 = serializers.CharField(write_only=True, required=True)

    def validate_prev_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError({"error": "현재 비밀번호가 일치하지 않습니다."})

    def validate(self, attrs):
        if attrs["password_1"] != attrs["password_2"]:
            raise serializers.ValidationError(
                {"error": "비밀번호1과 비밀번호2가 일치하지 않습니다"})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password_1"])
        instance.save()
        return instance
