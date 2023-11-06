##########################################################################################
##################################### REST_FRAMEWWORK #####################################
# from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
###########################################################################################
from django.http import JsonResponse
###########################################################################################
####################################### APP IMPORTS #######################################
from . import models
from . import serializers
###########################################################################################
########################################### SET ###########################################
@api_view(['POST'])
def setExame(request):
    if request.method == 'POST':
        novo_exame = request.data

        serializer = serializers.userExameArquivoSerializer(data=novo_exame)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class setExameArquivo(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        pdf_serializer = serializers.UploadedFileSerializer(data=request.data)

        if pdf_serializer.is_valid():
            pdf_serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            Response(pdf_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##########################################################################################
########################################### GET - LISTAS ###########################################
@api_view(['GET'])
def getPacientesFHIR(request):
    try:
        usuario = models.Usuario_autenticacao.objects.all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = serializers.pacienteSerializer(usuario, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def getExamesLista(request):
    try:
        exames = models.Usuario_exame_arquivo.objects.all()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = serializers.userExameArquivoSerializer(exames, many=True)
    return Response(serializer.data)

###########################################################################################
########################################### GET - BUSCA ###########################################
# Busca Paciente de acordo tipo de identificador enviado no POST
@api_view(['GET'])
def getPaciente(request):
    try:
        if request.GET['identificador_paciente'] and request.GET['tipo_identificador']:

            # Caso seja CPF, primeiro faz uma busca na tabela usuario_configuracao que vai retornar o id_usuario_autenticacao através da variavel user_id, através desse id, é feita a consulta na tabela usuario_autenticacao
            if request.GET['tipo_identificador'] == 'cpf':
                user_cpf = request.GET['identificador_paciente']
                try:
                    user_config = models.Usuario_configuracao.objects.get(cpf=user_cpf)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                
                user_cpf_serializer = serializers.userConfigSerializer(user_config)
                user_id = user_cpf_serializer.data['id_usuario_autenticacao']

                try:
                    usuario = models.Usuario_autenticacao.objects.get(id_usuario_autenticacao=user_id)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                
            # get por email
            if request.GET['tipo_identificador'] == 'email':
                usuario_email = request.GET['identificador_paciente']
                try:
                    usuario = models.Usuario_autenticacao.objects.get(email=usuario_email)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                
            # get por celular
            if request.GET['tipo_identificador'] == 'celular':
                usuario_celular = request.GET['identificador_paciente']
                try:
                    usuario = models.Usuario_autenticacao.objects.get(celular=usuario_celular)
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            
            # se chegou até aqui, encontrou os dados, então serializa eles e retorna pra requisição
            serializer = serializers.pacienteSerializer(usuario)
            return Response(serializer.data)
        
        # Caso não tenha os parametros da requisição, retorna erro 204 No Content
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Caso tenha algum problema na conexão, retorna 400 Bad Request
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getPacienteExameArquivo(request):

    if request.GET['id_paciente']:
        id_paciente = request.GET['id_paciente']

        try:
            exames = models.Usuario_exame_arquivo.objects.filter(id_usuario_autenticacao=id_paciente)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    serializer = serializers.userExameArquivoSerializer(exames, many=True)
    return Response(serializer.data)
