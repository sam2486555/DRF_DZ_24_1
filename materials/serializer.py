from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from materials.validators import UrlValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field="url")]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    course_subscription = serializers.SerializerMethodField()  # поле подписки на курс

    def get_course_subscription(self, obj):
        """ Метод вывода подписан ли пользователь на курс """
        return Subscription.objects.filter(course=obj, user=self.context['request'].user).exists()

    def get_lessons_count(self, instance):
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
