from rest_framework import serializers

from .models import * 
from .services.service_of_slug import text_to_slug
from .services.service_of_data_base import get_theme_by_slug, get_phor_by_slug, get_user_of_client_by_pk


class _FilterAnswerSerializer( serializers.ListSerializer ):
    """ Класс сериализатора, который убирает из общего списка Answers записи c parent_answer != None """

    def to_representation(self, data):
        data = data.filter( parent_answer = None )

        return super().to_representation(data)

class _ChildAnswerSerializer( serializers.Serializer ):
    """ Сериализатор для рекурсии и отображения дочерних Answers """

    def to_representation(self, value):
        serializer = _AnswerSerializer( value, context = self.context )

        return serializer.data

class _AnswerSerializer( serializers.ModelSerializer ):
    """ Сериализатор для Answers """

    child_answers = _ChildAnswerSerializer( many = True )
    creator = serializers.SlugRelatedField( slug_field = 'username', read_only = True ) 

    class Meta:
        list_serializer_class = _FilterAnswerSerializer
        model = Answers
        fields = ( 'creator', 'date_of_creation', 'is_correct', 'content', 'child_answers', 'pk' )

class CreateAnswerSerializer( serializers.ModelSerializer ):
    """ Сериализатор для создания экземпляров Answers модели """

    class Meta:
        model = Answers 
        fields = ( 'content', 'parent_answer', )

    def create(self, validated_data):
        slug_of_theme = self.context['view'].kwargs.get( 'slug_of_theme' )
        slug_of_phor = self.context['view'].kwargs.get( 'slug_of_phor' )
        pk_of_user_of_client = self.context['view'].kwargs.get( 'pk_of_user_of_client' )

        validated_data['creator'] = get_user_of_client_by_pk( pk_of_user_of_client )

        theme_of_phor = get_theme_by_slug( slug_of_theme )
        validated_data['phor'] = get_phor_by_slug( slug_of_phor, theme_of_phor )

        return super().create(validated_data)



class _ListPhorSerializer( serializers.ModelSerializer ):
    """ Сериализатор для экземпляров Phors модели """

    theme = serializers.SlugRelatedField( slug_field = 'slug', read_only = True )
    creator = serializers.SlugRelatedField( slug_field = 'username', read_only = True )

    class Meta:
        model = Phors 
        fields = ( 'title', 'slug', 'theme', 'creator', )

class PhorSerializer( serializers.ModelSerializer ):
    """ Сериализатор для экземпляра Phors модели """

    answers = _AnswerSerializer( many = True )

    theme = serializers.SlugRelatedField( slug_field = 'slug', read_only = True )
    creator = serializers.SlugRelatedField( slug_field = 'username', read_only = True )

    class Meta:
        model = Phors
        fields = ( 'title', 'creator', 'theme', 'date_of_creation', 'slug', 'description', 'answers', 'pk' )

class CreatePhorSerializer( serializers.ModelSerializer ):
    """ Сериализатор для создания экземпляра Phors модели """

    class Meta:
        model = Phors 
        fields = ( 'title', 'description', )

    def create(self, validated_data):
        slug_of_theme = self.context['view'].kwargs.get( 'slug_of_theme' )
        pk_of_user_of_client = self.context['view'].kwargs.get( 'pk_of_user_of_client' )

        validated_data['creator'] = get_user_of_client_by_pk( pk_of_user_of_client )

        validated_data['slug'] = text_to_slug( validated_data['title'] )
        validated_data['theme'] = get_theme_by_slug( slug_of_theme )

        return super().create(validated_data)



class ThemeSerializer( serializers.ModelSerializer ):
    """ Сериализатор для экземпляра Themes модели """

    phors = _ListPhorSerializer( many = True )

    class Meta:
        model = Themes 
        fields = ( 'title', 'slug', 'phors', 'pk' )

class ListThemeSerializer( serializers.ModelSerializer ):
    """ Сериализатор для экземпляров Themes модели """

    class Meta:
        model = Themes 
        fields = ( 'title', 'slug', )

class CreateThemeSerializer( serializers.ModelSerializer ):
    """ Сериализатор для создания экземпляра Themes модели """

    creator = serializers.HiddenField( default = serializers.CurrentUserDefault() )

    class Meta:
        model = Themes
        fields = ( 'title', 'creator' )

    def create(self, validated_data):
        validated_data['slug'] = text_to_slug( validated_data['title'] )

        return super().create(validated_data)



class UserOfClientSerializer( serializers.ModelSerializer ):
    """ Сериализатор для экземпляра UserOfClient модели """

    class Meta:
        model = UsersOfClient
        fields = '__all__'

class CreateUserOfClientSerializer( UserOfClientSerializer ):
    """ Сериализатор для создания экземпляра UserOfClient модели """

    client = serializers.HiddenField( default = serializers.CurrentUserDefault() )



class LogOfClientSerializer( serializers.ModelSerializer ):
    """ Сериализатор для экземпляра ( -ов ) LogOfClient модели """

    class Meta:
        model = LogOfClient
        fields = '__all__'


class LogOfUserOfClientSerializer( serializers.ModelSerializer ):
    """ Сериализатор для экземпляра ( -ов ) LogOfUserOfClient модели """

    class Meta:
        model = LogOfUserOfClient
        fields = '__all__'