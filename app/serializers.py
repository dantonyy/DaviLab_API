from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField
from . import models

class userAuthSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Usuario_autenticacao
        fields = [
            'id_usuario_autenticacao',
            'nome',
            'sobrenome',
            'celular',
            'email',
        ]

class userConfigSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Usuario_configuracao
        fields = '__all__'

class userExameArquivoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Usuario_exame_arquivo
        fields = '__all__'

class UploadedFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.UploadedFile
        fields = '__all__'

class pacienteSerializer(serializers.ModelSerializer):
    # Montagem campos FHIR Resource
    resourceType = serializers.CharField(default="Patient")
    identifier = serializers.SerializerMethodField()
    active = serializers.BooleanField(default=True)
    name = serializers.SerializerMethodField()
    telecom = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    birthDate = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    communication = serializers.SerializerMethodField() # communication[language] campo com cardinalidade 1..1
    link = serializers.SerializerMethodField() # 'contato de emergencia' campo com cardinalidade 1..1

    class Meta:
        model = models.Usuario_autenticacao
        fields = [
            'resourceType',
            'identifier',
            'active',
            'name',
            'telecom',
            'gender',
            'birthDate',
            'address',
            'communication',
            'link'
        ]
    
    #Buscar no model o campo que representa, nesta aplicação, o campo que será exportado nos padrões FHIR
    def get_identifier(self, instance):
        identifier = {
            'value' : instance.id_usuario_autenticacao
            }
        return identifier
    
    def get_name(self, instance):
        name = {
            'family'    : instance.sobrenome,
            'given'     : instance.nome
        }
        return name
    
    def get_telecom(self, instance):
        # http://build.fhir.org/valueset-contact-point-system.html
        telecom = ( #Cada valor abaixo é um contact-point diferente
            {
                'system' : 'email',
                'value' : instance.email
            },
            {
                'system' : 'phone',
                'value' : instance.celular
            }
        )
        return telecom

    def get_gender(self, instance):
        #Code-system: http://hl7.org/fhir/administrative-gender
        user_config_data = models.Usuario_configuracao.objects.get(id_usuario_autenticacao=instance.id_usuario_autenticacao)
        genero = user_config_data.genero

        if genero == 'Masculino':
            genero = 'male'
        if genero == 'Feminino':
            genero = 'female'
        if genero == 'Outro':
            genero = 'other'

        gender = genero
        return gender

    def get_birthDate(self, instance):
        user_config_data = models.Usuario_configuracao.objects.get(id_usuario_autenticacao=instance.id_usuario_autenticacao)
        birthDate = user_config_data.data_nascimento
        return birthDate
    
    def get_address(self, instance):
        user_config_data = models.Usuario_configuracao.objects.get(id_usuario_autenticacao=instance.id_usuario_autenticacao)
        address = user_config_data.endereco
        return address
    
    def get_communication(self, instance):
        user_config_data = models.Usuario_configuracao.objects.get(id_usuario_autenticacao=instance.id_usuario_autenticacao)

        # Code-systems:
        # https://www.iso.org/obp/ui/#iso:code:3166:BR
        # https://unstats.un.org/unsd/methodology/m49/

        if user_config_data.nacionalidade == 'BR':
            language = (
                {
                    'coding' : 
                    {
                        "system": "https://www.iso.org/obp/ui/#iso:code:3166:BR",
                        "code": "pt",
                        "display": "Portuguese"
                    },
                    'preferred' : True
                }
            )
            communication = language
        return communication

    def get_link(self, instance):
        reference = (
            {
                'reference' : {
                    'reference' : 'internal',
                    'type' : 'Patient',
                    # 'identifier' : instance.contato_emergencia
                }
            },
            {
                'type' : {
                    'system' : 'http://hl7.org/fhir/link-type',
                    'code' : 'refer' # 	replaced-by | replaces | refer | seealso
                }
            }
        )

        link = reference
        return link
    
    # Monta os campos com os valores vindos do banco
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
